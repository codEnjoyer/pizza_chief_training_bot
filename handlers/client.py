from aiogram import types, Dispatcher
from aiogram.utils.exceptions import CantInitiateConversation

from bot_create import bot

from keyboards import kb_client
from database import sqlite_db


async def start_command(message: types.Message):
    user_id = message.from_user.id
    try:
        await bot.send_message(user_id, 'Поехали!', reply_markup=kb_client)
    except CantInitiateConversation:
        await message.reply("Общение с ботом в ЛС, напишите ему:\nhttps://t.me/Pizza_chief_training_bot")


async def help_command(message: types.Message):
    await start_command(message)


async def working_hours_command(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(user_id, "Свет внутри меня не горит, но я всё ещё работаю.")


async def geolocation_command(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(user_id, 'улица Малышева, 21/4')


async def menu_command(message: types.Message):
    user_id = message.from_user.id
    pizzas = await sqlite_db.get_values()
    for pizza in pizzas:
        await bot.send_photo(user_id, pizza[0], f'{pizza[1]}\n'
                                                f'Описание: {pizza[2]}\n'
                                                f'Цена: {pizza[3]}')


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(start_command, commands=['start'])
    dispatcher.register_message_handler(help_command, commands=['help'])
    dispatcher.register_message_handler(working_hours_command, commands=['Режим_работы'])
    dispatcher.register_message_handler(geolocation_command, commands=['Расположение'])
    dispatcher.register_message_handler(menu_command, commands=['Меню'])
