import sqlite3

from aiogram.dispatcher import FSMContext


def start():
    global db, cursor
    db = sqlite3.connect('pizza_menu.db')
    cursor = db.cursor()
    if db:
        print("База данных успешно подключена")
    db.execute("""CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)""")
    db.commit()


async def add_row(state: FSMContext):
    async with state.proxy() as data:
        cursor.execute("""INSERT INTO menu VALUES (?, ?, ?, ?)""", tuple(data.values()))
        db.commit()


async def get_values() -> list:
    return cursor.execute("SELECT * FROM menu").fetchall()


async def delete_item(name: str):
    cursor.execute("""DELETE FROM menu WHERE name == ?""", (name,))
    db.commit()
