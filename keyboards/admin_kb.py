from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

load_button = KeyboardButton("/Добавить_пиццу")
delete_button = KeyboardButton("/Удалить")
menu_button = KeyboardButton("/Меню")

kb_admin = ReplyKeyboardMarkup()

kb_admin.row(load_button, delete_button, menu_button)
