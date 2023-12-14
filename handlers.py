from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import flags

import kb
import text
import utils
from states import Notes as notes_state

router = Router()


# Функции записи данных
@router.callback_query(F.data == "add_note")
async def add_note(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(text.add_note, reply_markup=kb.iexit_kb) 
    await state.set_state(notes_state.waiting_for_note)   

@router.message(notes_state.waiting_for_note)
async def save_note_handler(msg: Message, state: FSMContext):
    note_text = msg.text
    user_id = msg.from_user.id

    # Сохраняем заметку в базу данных
    await msg.answer("Сохраняем в базу данных..")
    # Сбрасываем состояние после сохранения заметки
    await state.clear()
    await msg.answer("Заметка успешно сохранена!")
    await msg.answer(text.menu, reply_markup=kb.menu)

# Функции просмотра даных
@router.callback_query(F.data == "view_note_list")
async def view_note(clbck: CallbackQuery):
    await clbck.message.answer(text.view_note, reply_markup=kb.iexit_kb)


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

    