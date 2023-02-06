from aiogram import types, Dispatcher


async def echo_send(message: types.Message):
    # await message.answer(message.text)
    # await message.reply(message.text)
    pass


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(echo_send)
