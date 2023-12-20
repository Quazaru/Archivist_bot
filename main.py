# python
import asyncio
import logging
# telegram
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage


# postgresql
import psycopg2

# local files
import config

from handlers import collections_handler, notes_handler, files_handler, commands_handler, menu_handler
from handlers.collections_handler import collections_router
from handlers.notes_handler import notes_router
from handlers.files_handler import files_router
from handlers.commands_handler import commands_router
from handlers.menu_handler import menu_router
import utils_sql

db_handler = None
db_connected = False
try:
    db_handler = utils_sql.DBHandler()
    db_connected = True
except:
    print("[ERROR] DBHandler error! Unable to connect to the database.")

if db_connected:
    # В случае успешного подключения к базе данных запускаем бота
    db_handler.database_init()
    async def main():
        bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
        dp = Dispatcher(storage=MemoryStorage())
        dp.include_router(menu_handler.menu_router)
        dp.include_router(commands_handler.commands_router)
        dp.include_router(collections_handler.collections_router)
        dp.include_router(notes_handler.notes_router)
        dp.include_router(files_handler.files_router) 
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    if __name__ == "__main__":
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
else:
    # В случае неудачного подключения к базе данных выходим из программы
    print("[ERROR] Bot cannot be started due to failed database connection.")
