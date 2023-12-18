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
import utils_sql
import states
import config
from utils_sql import DBHandler
router = Router()
db_handler = DBHandler()

# Функции записи данных
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
    await msg.answer(f"Collection `{collection_name}` created by {msg.from_user.full_name}", reply_markup=kb.iexit_kb) 


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
    await msg.answer("Заметка успешно сохранена!")
    await msg.answer(text.menu, reply_markup=kb.menu)

# Функции просмотра даных
@router.callback_query(F.data == "view_note_list")
async def view_note(clbck: CallbackQuery):
    user_id = clbck.from_user.id
    notes = db_handler.table_select_all("Notes")

    if not notes:
        await clbck.message.answer("Нет доступных заметок для этой коллекции.")
        return
    result_message = "Ваши заметки: \n"
    for idx, note in enumerate(notes):
        result_message += f"->{idx}. <b>{note["Name"]}</b>\n"
        result_message += f"{note["NoteText"]}\n\n"

    await clbck.message.answer(result_message, reply_markup=kb.iexit_kb)

        
@router.callback_query(F.data == "view_collection_list")
async def view_collection_list(clbck: CallbackQuery):
    user_id = "1"  

    collections = utils_sql.get_collection_list(user_id)

    if collections:
        buttons = [
            InlineKeyboardButton(
                text=collection[2],  
                callback_data=f"view_collection_{collection[0]}" 
            )
            for collection in collections
        ]

        rows = [buttons[i:i + 1] for i in range(0, len(buttons), 1)]  

        keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
        await clbck.message.answer("Выберите коллекцию:", reply_markup=keyboard)
    else:
        await clbck.message.answer("У вас нет доступных коллекций.")



# Навигация по меню
@router.message(Command("start"))
async def start_handler(msg: Message):
    tg_userID = msg.from_user.id
    if not db_handler.table_select("Users", ("UserID", "=", tg_userID)):
        db_handler.table_insert("Users", {"UserID": tg_userID, "SelectedCollectionID": 1})
        db_handler.table_insert("Collections", {"CreationTime": "00-00-00", "UserID": tg_userID, "Name": "FirstCollection"})
        newCollectionID = db_handler.table_select("Collections", ("UserID", "=", tg_userID))[0]["CollectionID"]
        db_handler.table_update(table_name="Users", update_dict={"SelectedCollectionID": newCollectionID}, condition_tuple=("UserID", "=", tg_userID))
    print(" PRINT DB \n")
    print(db_handler.table_select_all("users"))
    print(db_handler.table_select_all("collections"))
    await msg.answer(text.greet.format(user=html.quote(msg.from_user.full_name)), reply_markup=kb.menu)



@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(clbck: CallbackQuery):
    await clbck.message.answer(text.menu, reply_markup=kb.menu)
@router.message(F.text == "Меню")
@router.message(F.text == "меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)
    userId = await msg.from_user.id
    config.MAIN_COLLECTION_ID = userId

    