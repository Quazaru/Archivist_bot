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
import utils


# SQL handle
utils.init_archivist_database();

# Telegram handle
async def main():
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML) # HTML для корректной разметки
    dp = Dispatcher(storage=MemoryStorage()) # Всё, что не добавили в бд - чистим
    dp.include_router(router) 
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
