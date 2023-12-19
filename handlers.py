from datetime import datetime

from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.types.callback_query import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram import flags
from aiogram.enums import ParseMode
from aiogram.utils.formatting import (Bold, as_list, as_marked_section, as_key_value, HashTag)
from aiogram import html


import kb
import text
import states
import queries_sql
from utils_sql import DBHandler
router = Router()
db_handler = DBHandler()

# Файлы
@router.message(F.sticker)
@router.message(F.animation)
@router.message(F.photo)
@router.message(F.voice)
@router.message(F.photo)
async def still_developing(msg: Message):
    
    await msg.answer("Обработка такого формата ещё в разработке 💀💀💀", reply_markup=kb.iexit_kb)

# Коллекции 
@router.callback_query(F.data == "view_collection_list")
async def view_collection_list(clbck: CallbackQuery):
    user_id = clbck.from_user.id  

    collections = db_handler.table_select("Collections", ("UserID", "=", user_id))
    if not collections:
        await clbck.message.answer("У вас нет доступных коллекций.")
    result_message = "<b>Ваши коллекции:</b> \n" 
    for idx, collection in enumerate(collections):
        result_message += f"\n<b>[{idx+1}] -></b> {html.quote(collection["Name"])}" 
    await clbck.message.edit_text(result_message, reply_markup=kb.sorting_menu)
        
@router.callback_query(F.data == "add_collection") #####
async def add_collection(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(text.add_collection, reply_markup=kb.iexit_kb) 
    await state.set_state(states.Collections.waiting_for_name)   

@router.message(states.Collections.waiting_for_name)
async def add_collection_handler(msg: Message, state: FSMContext):
    collection_name = msg.text
    user_id = msg.from_user.id
    creation_time = "00-00-00"
    db_handler.table_insert("Collections", {
        "Name": collection_name,
        "CreationTime": creation_time,
        "UserID": user_id
    })
    await state.clear()
    await msg.answer(f"Collection `{html.quote(collection_name)}` created by {html.quote(msg.from_user.full_name)}", reply_markup=kb.iexit_kb) 
@router.callback_query(F.data == "collections_sort_by_name")
async def collections_sort_by_name(mag: Message):
    user_id = mag.from_user.id  
    collections = db_handler.table_select_new("Collections", ("UserID", "=", user_id), "Name", False)
    if not collections:
        await mag.message.answer("У вас нет доступных коллекций.")
    result_message = "<b>Ваши коллекции:</b> \n" 
    for idx, collection in enumerate(collections):
        result_message += f"\n<b>[{idx+1}] -></b> {html.quote(collection["Name"])}" 
    await mag.message.edit_text(result_message, reply_markup=kb.sorting_menu)

@router.callback_query(F.data == "collections_sort_by_creationDate")
async def collections_sort_by_name(mag: Message):
    user_id = mag.from_user.id  
    collections = db_handler.table_select_new("Collections", ("UserID", "=", user_id), "CollectionID", False)
    if not collections:
        await mag.message.answer("У вас нет доступных коллекций.")
    result_message = "<b>Ваши коллекции:</b> \n" 
    for idx, collection in enumerate(collections):
        result_message += f"\n<b>[{idx+1}] -></b> {html.quote(collection["Name"])}" 
    await mag.message.edit_text(result_message, reply_markup=kb.sorting_menu)



# Заметки
@router.callback_query(F.data == "view_note_list")
async def view_note(clbck: CallbackQuery):
    user_id = clbck.from_user.id
    notes = db_handler.table_select_all("Notes")

    if not notes:
        await clbck.message.edit_text("Нет доступных заметок для этой коллекции.", reply_markup=kb.iexit_kb)
        return
    result_message = "Ваши заметки: \n"
    for idx, note in enumerate(notes):
        result_message += f"->{idx+1}. <b>{note["Name"]}</b>\n"
        result_message += f"{note["NoteText"]}\n\n"

    await clbck.message.edit_text(result_message, reply_markup=kb.iexit_kb)

@router.callback_query(F.data == "add_note")
async def add_note(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(text.add_note, reply_markup=kb.iexit_kb) 
    await state.set_state(states.Notes.waiting_for_note)   

@router.message(states.Notes.waiting_for_note)
async def add_note_handler(msg: Message, state: FSMContext):
    note_text = msg.text
    user_id = msg.from_user.id
    creation_time = "00-00-00"
    collection_id = db_handler.table_select("Users", ("UserID", "=", user_id))[0]["SelectedCollectionID"]
    db_handler.table_insert("Notes", {
        "Name": "Untilted",
        "CreationTime": creation_time,
        "NoteText": note_text,
        "CollectionID": collection_id,
    })
    await state.clear()
    await msg.answer(text.menu, reply_markup=kb.menu)




# Навигация по меню
@router.message(Command("start"))
async def start_handler(msg: Message):
    # инициализация нового пользователя
    tg_userID = msg.from_user.id
    if not db_handler.table_select("Users", ("UserID", "=", tg_userID)):
        db_handler.table_insert("Users", {"UserID": tg_userID, "SelectedCollectionID": 1})
        db_handler.table_insert("Collections", {"CreationTime": "00-00-00", "UserID": tg_userID, "Name": "FirstCollection"})
        newCollectionID = db_handler.table_select("Collections", ("UserID", "=", tg_userID))[0]["CollectionID"]
        db_handler.table_update(table_name="Users", update_dict={"SelectedCollectionID": newCollectionID}, condition_tuple=("UserID", "=", tg_userID))
    print(" PRINT DB \n")
    print(db_handler.table_select_all("users"))
    print(db_handler.table_select_all("collections"))
    print(" TESTING SQL \n\n\n\n")
    print(queries_sql.QueryHelper.generate_query_select_new())
    await msg.answer(text.greet.format(user=html.quote(msg.from_user.full_name)), reply_markup=kb.menu)



@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(clbck: CallbackQuery):
    user_id = clbck.from_user.id
    SelectedCollectionID = db_handler.table_select("Users", ("UserID", "=", user_id))[0]["SelectedCollectionID"]
    SelectedCollectionName = db_handler.table_select("Collections", ("CollectionID", "=", SelectedCollectionID))[0]["Name"]
    await clbck.message.edit_text(text.menu.format(html.quote(CollectionName=SelectedCollectionName)), reply_markup=kb.menu)


    