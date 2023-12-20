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
menu_router = Router()

# Навигация по меню
@menu_router.message(Command("start"))
async def start_handler(msg: Message):
    # инициализация нового пользователя
    tg_userID = msg.from_user.id
    if not db_handler.table_select("Users", ("UserID", "=", tg_userID)):
        db_handler.table_insert("Users", {"UserID": tg_userID, "SelectedCollectionID": 1})
        db_handler.table_insert("Collections", {"CreationTimestamp": DateHelper.getTimestamp(), "UserID": tg_userID, "Name": "Первая коллекция"})
        newCollectionID = db_handler.table_select("Collections", ("UserID", "=", tg_userID))[0]["CollectionID"]
        db_handler.table_update(table_name="Users", update_dict={"SelectedCollectionID": newCollectionID}, condition_tuple=("UserID", "=", tg_userID))
    await msg.answer(text.menu_greet.format(user=html.quote(msg.from_user.full_name)), reply_markup=kb.menu)

@menu_router.message(Command("menu"))
@menu_router.callback_query(F.data == "back_to_menu")
async def back_to_menu(clbck: CallbackQuery, state=FSMContext):
    user_id = clbck.from_user.id
    SelectedCollectionID = db_handler.table_select("Users", ("UserID", "=", user_id))[0]["SelectedCollectionID"]
    SelectedCollectionName = db_handler.table_select("Collections", ("CollectionID", "=", SelectedCollectionID))[0]["Name"]
    await clbck.message.edit_text(html.quote(text.menu_header.format(CollectionName=SelectedCollectionName)), reply_markup=kb.menu)
    await state.clear()