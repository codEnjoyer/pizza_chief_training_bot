from aiogram.utils import executor

from handlers import client, admin, other

from bot_create import dp
from database import sqlite_db

client.register_handlers(dp)
admin.register_handlers(dp)
other.register_handlers(dp)


async def on_startup(_):
    print("Бот вышел в онлайн.")
    sqlite_db.start()


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
