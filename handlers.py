from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types.callback_query import CallbackQuery
from aiogram import flags



import kb
import text

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)

@router.callback_query(F.data == "add_note")
async def add_note(clbck: CallbackQuery):
    await clbck.message.answer(text.add_note, reply_markup=kb.add_note_kb)    
@router.callback_query(F.data == "view_note_list")
async def view_note(clbck: CallbackQuery):
    await clbck.message.answer(text.view_note, reply_markup=kb.iexit_kb)


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(clbck: CallbackQuery):
    await clbck.message.answer(text.menu, reply_markup=kb.menu)
@router.message(F.text == "Меню")
@router.message(F.text == "меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)

    