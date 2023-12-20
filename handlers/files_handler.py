# imports
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
files_router = Router()

# Файлы
@files_router.message(F.sticker)
@files_router.message(F.animation)
@files_router.message(F.photo)
@files_router.message(F.voice)
@files_router.message(F.photo)
async def still_developing(msg: Message):
    await msg.answer(text.util_still_developing, reply_markup=kb.iexit_kb)