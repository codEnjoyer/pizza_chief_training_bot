from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot_create import bot, dp
from database import sqlite_db
from keyboards import kb_admin

ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def start_admin_mode(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(ID, "Слушаю и повинуюсь, хозяин.", reply_markup=kb_admin)
    await message.delete()


# region StateMachine
async def start_command(message: types.Message):
    if message.from_user.id != ID:
        return
    await FSMAdmin.photo.set()
    await message.answer("Загрузите фотографию")


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["photo"] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer("Введите название")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    await FSMAdmin.next()
    await message.answer("Введите описание")


async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["description"] = message.text
    await FSMAdmin.next()
    await message.answer("Введите цену")


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["price"] = float(message.text)

    await sqlite_db.add_row(state)
    await state.finish()
    await message.answer("Отлично, пицца была добавлена в меню!")


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Хорошо, формирование пиццы отменено")


async def delete_pizzas(message: types.Message):
    user_id = message.from_user.id
    if user_id == ID:
        pizzas = await sqlite_db.get_values()
        for pizza in pizzas:
            inline_delete_markup = InlineKeyboardMarkup().add(
                InlineKeyboardButton(f"Удалить {pizza[1]}", callback_data=f"delete {pizza[1]}"))
            await bot.send_photo(user_id, pizza[0], f'{pizza[1]}\n'
                                                    f'Описание: {pizza[2]}\n'
                                                    f'Цена: {pizza[3]}', reply_markup=inline_delete_markup)


@dp.callback_query_handler(Text(startswith="delete "))
async def delete_pizza_callback_handler(callback_query: types.CallbackQuery):
    pizza_name = callback_query.data.split(' ')[1]
    await sqlite_db.delete_item(pizza_name)
    await callback_query.answer(text=f"{pizza_name} была удалена", show_alert=True)


# endregion StateMachine

def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(start_admin_mode, commands=["admin"], is_chat_admin=True)

    dispatcher.register_message_handler(start_command, commands=["Добавить_пиццу"], state=None)
    dispatcher.register_message_handler(load_photo, content_types=["photo"], state=FSMAdmin.photo)
    dispatcher.register_message_handler(load_name, state=FSMAdmin.name)
    dispatcher.register_message_handler(load_description, state=FSMAdmin.description)
    dispatcher.register_message_handler(load_price, state=FSMAdmin.price)

    dispatcher.register_message_handler(delete_pizzas, commands=["Удалить"])

    dispatcher.register_message_handler(cancel_handler, state='*', commands=["Отмена"])
    dispatcher.register_message_handler(cancel_handler, Text(equals="отмена", ignore_case=True), state='*')
