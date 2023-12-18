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
from handlers import router
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
        dp.include_router(router) 
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    if __name__ == "__main__":
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
else:
    # В случае неудачного подключения к базе данных выходим из программы
    print("[ERROR] Bot cannot be started due to failed database connection.")
