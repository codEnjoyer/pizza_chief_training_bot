from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from os import getenv

bot = Bot(token=getenv("TOKEN"))

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
