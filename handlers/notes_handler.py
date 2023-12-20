# imports
import hashlib
# aiogram
from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import flags
from aiogram import html
# Files
import kb
import text
import states
from utils_sql import DBHandler
from utils_date import DateHelper


notes_router = Router()
db_handler = DBHandler()

def formatNotesShowOutput(notes, note_visible_text_size=80):
    result_message = "📄 Ваши заметки: \n"
    for idx, note in enumerate(notes):
        result_message += f"{idx+1}. {text.extra_arror_right} <b>{note["Name"]}</b>\n"
        result_message += f"{note["NoteText"][:note_visible_text_size]}{"..." if len(note["NoteText"]) > note_visible_text_size-3 else ""}\n\n"
    return result_message

# Заметки
@notes_router.callback_query(F.data == text.clbck_notes_set_text)
async def add_note(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(text.note_add_start, reply_markup=kb.iexit_kb) 
    await state.set_state(states.Notes.set_text)   

@notes_router.message(states.Notes.set_text)
async def add_note_handler(msg: Message, state: FSMContext):
    note_text = msg.text
    user_id = msg.from_user.id
    note_creation_time = DateHelper.getTimestamp()
    note_name = DateHelper.getStr(timestamp=note_creation_time)
    collection_id = db_handler.table_select("Users", ("UserID", "=", user_id))[0]["SelectedCollectionID"]
    db_handler.table_insert("Notes", {
        "Name": note_name,
        "CreationTimestamp": note_creation_time,
        "NoteText": note_text,
        "CollectionID": collection_id,
    })
    await state.clear()
    await msg.answer(text.menu_header, reply_markup=kb.menu)

## Notes menu
@notes_router.callback_query(F.data == text.clbck_notes_menu_open)
async def view_note(clbck: CallbackQuery, state: FSMContext):
    user_id = clbck.from_user.id
    # Получаем заметки из выбранной коллекции
    selected_collection_id = db_handler.table_select("Users", condition_tuple=("UserID", "=", user_id))[0]["SelectedCollectionID"]
    notes = db_handler.table_select("Notes", condition_tuple=("CollectionID", "=", selected_collection_id))
    if not notes:
        await clbck.message.edit_text("Нет доступных заметок для этой коллекции.", reply_markup=kb.iexit_kb)
        return
    result_message = formatNotesShowOutput(notes)
    result_message_hash = hashlib.sha256(result_message.encode()).hexdigest()
    sent_message = await clbck.message.edit_text(result_message, reply_markup=kb.sorting_menu)
    await state.update_data(sent_message_id=sent_message.message_id, last_notes_output_hash=result_message_hash)
    await state.set_state(states.Menu.is_notes)
# Sorting
@notes_router.callback_query(states.Menu.is_notes, F.data.in_({"sort_by_name", "sort_by_time"}), F.data.as_("sort_type"))
async def notes_sort(clbck: CallbackQuery, state: FSMContext, sort_type: str):
    # Собираем данные
    user_id = clbck.from_user.id
    isDESC = False
    state_data = await state.get_data()
    current_sort = state_data.get("current_notes_sort")
    current_sort_DESC = state_data.get("current_notes_sort_DESC")
    message_id = state_data.get("sent_message_id")
    last_notes_output_hash = state_data.get("last_notes_output_hash")
    # Проверка на нулевые значения
    if not current_sort:
        current_sort = sort_type
        current_sort_DESC = isDESC
    # Если сортировка одна и та же, меняем порядок сортировки
    if(current_sort == sort_type):
        isDESC = not current_sort_DESC
    # Определяем параметры запроса sql   
    order_by_field = "Notes.\"Name\"" if sort_type == "sort_by_name" else "Notes.\"NoteID\""
    selected_collection_id = db_handler.table_select("Users", condition_tuple=("UserID", "=", user_id))[0]["SelectedCollectionID"]
    # Генерируем выходные данные
    notes = db_handler.table_select("Notes", condition_tuple=("CollectionID", "=", selected_collection_id), orderByField=order_by_field, isDESC=isDESC)
    if not notes:
        await clbck.message.edit_text("Нет доступных заметок для этой коллекции.", reply_markup=kb.iexit_kb)
        return
    result_message = formatNotesShowOutput(notes)
    result_message_hash = hashlib.sha256(result_message.encode()).hexdigest()
    if(result_message_hash != last_notes_output_hash):
            await clbck.bot.edit_message_text(chat_id=clbck.from_user.id, message_id=message_id,text=result_message, reply_markup=kb.sorting_menu)
    await state.update_data(current_notes_sort=sort_type, current_notes_sort_DESC=isDESC, last_notes_output_hash=result_message_hash) # Сохраняем текущий тип и порядок сортировки