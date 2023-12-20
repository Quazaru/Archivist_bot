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

db_handler = DBHandler()
collections_router = Router()

def formatCollectionsShowOutput(collections) -> str:
    result_message = text.collection_menu_header
    for collection in collections:
            result_message += f"\n{text.extra_arror_right} {html.quote(collection["Name"])}" 
    return result_message

@collections_router.callback_query(F.data == text.clbck_collections_menu_open)
async def view_collection_list(clbck: CallbackQuery, state: FSMContext):
    user_id = clbck.from_user.id  
    collections = db_handler.table_select("Collections", condition_tuple=("UserID", "=", user_id))
    if not collections:
        await clbck.message.answer(text.collection_empty)
    result_message = formatCollectionsShowOutput(collections)
    result_message_hash = hashlib.sha256(result_message.encode()).hexdigest()
    sent_message = await clbck.message.edit_text(result_message, reply_markup=kb.sorting_menu)
    await state.update_data(sent_message_id=sent_message.message_id, last_collections_output_hash=result_message_hash)
    await state.set_state(states.Menu.is_collections)


@collections_router.callback_query(F.data == text.clbck_collections_set_name)
async def add_collection(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(text.collection_add_start, reply_markup=kb.iexit_kb) 
    await state.set_state(states.Collections.set_name)   
@collections_router.message(states.Collections.set_name)
async def add_collection_handler(msg: Message, state: FSMContext):
    collection_name = msg.text
    user_id = msg.from_user.id
    creation_time = DateHelper.getTimestamp()
    db_handler.table_insert("Collections", {
        "Name": collection_name,
        "CreationTimestamp": creation_time,
        "UserID": user_id
    })
    await state.clear()
    await msg.answer(f"Collection `{html.quote(collection_name)}` created by {html.quote(msg.from_user.full_name)}", reply_markup=kb.iexit_kb) 

@collections_router.callback_query(states.Menu.is_collections, F.data.in_({"sort_by_name", "sort_by_time"}), F.data.as_("sort_type"))
async def collections_sort(clbck: CallbackQuery, state: FSMContext, sort_type: str):
    # Собираем данные
    isDESC = False
    user_id = clbck.from_user.id
    state_data = await state.get_data() # Получаем данные из FSM
    current_sort = state_data.get("current_collection_sort")
    current_sort_DESC = state_data.get("current_collection_sort_DESC")
    message_id = state_data.get("sent_message_id") # Получаем айди сообщения для редактирование, переданное при открытии меню коллекций
    last_collections_output_hash = state_data.get("last_collections_output_hash")
    # Проверка на нулевые значение
    if not current_sort:
        current_sort = sort_type
        current_sort_DESC = isDESC
    # Если сортировка одна и та же, то меняем DESC (По убыванию\По возрастанию)
    if(current_sort == sort_type):
        isDESC = not current_sort_DESC
    orderByField = "Collections.\"CollectionID\"" if sort_type == "sort_by_time" else "Collections.\"Name\"" # Настраиваем сортировку
    collections = db_handler.table_select("Collections", condition_tuple=("UserID", "=", user_id),
                                           orderByField=orderByField, isDESC=isDESC)
    if not collections:
        await clbck.message.answer(text.collection_empty, reply_markup=kb.iexit_kb) # Если в коллекции пусто, уведомляем об этом пользователя
    result_message = formatCollectionsShowOutput(collections) # Получаем отформатированный список коллекций в виде текста для сообщения
    result_message_hash = hashlib.sha256(result_message.encode()).hexdigest()
    if (last_collections_output_hash != result_message_hash ):
        await clbck.bot.edit_message_text(chat_id=clbck.from_user.id, message_id=message_id, text=result_message, reply_markup=kb.sorting_menu)
    await state.update_data(current_collection_sort=sort_type, current_collection_sort_DESC=isDESC,
                            last_collections_output_hash=last_collections_output_hash) # Сохраняем текущий тип и порядок сортировки