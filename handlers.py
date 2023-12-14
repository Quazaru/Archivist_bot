from datetime import datetime

from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types.callback_query import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram import flags

import kb
import text
import utils
import states

router = Router()


# Функции записи данных
@router.callback_query(F.data == "add_collection") #####
async def add_collection(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(text.add_collection, reply_markup=kb.iexit_kb) 
    await state.set_state(states.Collections.waiting_for_name)   

@router.message(states.Collections.waiting_for_name)
async def add_collection_handler(msg: Message, state: FSMContext):
    collection_name = msg.text
    user_id = msg.from_user.id

    utils.add_collection(user_id=user_id, name=collection_name)

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

    # Сохраняем заметку в базу данных
    await msg.answer("Сохраняем в базу данных..")
    utils.add_note('Base Collection', user_id=user_id, note_text=note_text)
    # Сбрасываем состояние после сохранения заметки
    await state.clear()
    await msg.answer("Заметка успешно сохранена!")
    await msg.answer(text.menu, reply_markup=kb.menu)

# Функции просмотра даных
@router.callback_query(F.data == "view_note_list")
async def view_note(clbck: CallbackQuery):
    collection_id = 1  
    notes = utils.get_notes(collection_id)

    if notes:
        buttons = [
            InlineKeyboardButton(
                text=note[3][:20] + "..." if len(note[3]) > 20 else note[3],  
                callback_data=f"view_note_{note[0]}" 
            )
            for note in notes
        ]
        
        rows = [buttons[i:i + 4] for i in range(0, len(buttons), 4)]  # Разбиваем кнопки по 4 в каждой строке

        keyboard = InlineKeyboardMarkup(inline_keyboard=rows)  # Формируем клавиатуру из строк с кнопками

        await clbck.message.answer("Выберите заметку:", reply_markup=keyboard)
    else:
        await clbck.message.answer("Нет доступных заметок для этой коллекции.")

@router.callback_query(F.data == "view_collection_list")
async def view_collection_list(clbck: CallbackQuery):
    user_id = "1"  

    collections = utils.get_collection_list(user_id)

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
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(clbck: CallbackQuery):
    await clbck.message.answer(text.menu, reply_markup=kb.menu)
@router.message(F.text == "Меню")
@router.message(F.text == "меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)

    