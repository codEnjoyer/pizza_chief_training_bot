from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

help_button = KeyboardButton("/help")
working_hours_button = KeyboardButton("/Режим_работы")
geolocation_button = KeyboardButton("/Расположение")
menu_button = KeyboardButton("/Меню")
send_contacts_button = KeyboardButton("Поделиться номером телефона", request_contact=True)
send_geolocation = KeyboardButton("Отправить текущее местоположение", request_location=True)

kb_client = ReplyKeyboardMarkup()

kb_client\
    .row(help_button, working_hours_button)\
    .row(geolocation_button, menu_button)\
    .row(send_contacts_button, send_geolocation)
