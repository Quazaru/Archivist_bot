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
commands_router = Router()

# Команды
@commands_router.message(Command("test"))
async def test(msg: Message):
    # Test new select func
    query1 = db_handler.table_select("Users", (("UserID", "=", 1231231231), ("SelectedCollectionID", ">", "2")), "SelectedCollectionID", False)
    query2 = db_handler.table_select("Users", orderByField="SelectedCollectionID")
    query3 = db_handler.table_select("Users")
    print(query1)
    print(query2)
    print(query3)
    print("__ [TESTING] NEW SELECT")
    await msg.answer(query1, reply_markup=kb.iexit_kb)
    await msg.answer(query2, reply_markup=kb.iexit_kb)
    await msg.answer(query3, reply_markup=kb.iexit_kb)