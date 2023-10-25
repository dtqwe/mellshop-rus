
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter
import app.keyboards as kb

import sqlite3
import datetime

router = Router()

from bot import admin_id

class Admin(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in [admin_id]

# Инициализация SQLite базы данных для пользователей
conn = sqlite3.connect("bot_users.db")
cursor = conn.cursor()

# Создание таблицы для хранения данных о пользователях
cursor.execute("CREATE TABLE IF NOT EXISTS bot_users (user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT, last_name TEXT)")
conn.commit()

# Инициализация SQLite базы данных для оценок
conn_ratings = sqlite3.connect("bot_ratings.db")
cursor_ratings = conn_ratings.cursor()

# Создание таблицы для хранения оценок
cursor_ratings.execute("""
    CREATE TABLE IF NOT EXISTS ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        date TIMESTAMP,
        rate INTEGER
    )
""")
conn_ratings.commit()

@router.message(Admin(), F.text == '/admin')
async def cmd_admin(message:Message):
    await message.answer(f'Привет {message.from_user.first_name}, ты админ')
    # Извлечение данных о пользователях, которые нажимали на /start
    cursor.execute("SELECT user_id, username, first_name, last_name FROM bot_users WHERE NOT username IS NULL")
    user_data = cursor.fetchall()
    
    if not user_data:
        await message.answer("Пока нет данных о пользователях, нажавших на /start.")
    else:
        admin_message = "Логи пользователей, которые нажимали на /start:\n\n"
        for user in user_data:
            user_id, username, first_name, last_name = user
            admin_message += f"User ID: {user_id}, Username: {username}, Имя: {first_name}, Фамилия: {last_name}\n"
        
        await message.answer(admin_message)

@router.message(Admin(), F.text == '/showrate')
async def view_ratings(message: Message):
    conn = sqlite3.connect("bot_ratings.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username, date, rate FROM ratings")
    ratings = cursor.fetchall()
    conn.close()

    if ratings:
        ratings_text = "\n".join([f"User ID: {row[0]}, Username: {row[1]}, Дата: {row[2]}, Оценка: {row[3]}" for row in ratings])
        await message.answer(f"Оценки пользователей:\n{ratings_text}")
    else:
        await message.answer("Пока нет оценок от пользователей.")


@router.message(F.text == '/start')
async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    # Проверка, не существует ли уже запись о пользователе в базе данных
    cursor.execute("SELECT user_id FROM bot_users WHERE user_id = ?", (user_id,))
    existing_user = cursor.fetchone()
    if not existing_user:
        cursor.execute("INSERT INTO bot_users (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)",
                       (user_id, username, first_name, last_name))
        conn.commit()

    await message.answer_photo(photo='https://ibb.co.com/fknFX72', caption=f'Привет, {message.from_user.first_name}, Добро пожаловать в магазин mellStore!', reply_markup=kb.main)


@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выбери категорию:', reply_markup=kb.catalog)


@router.callback_query(F.data == 'dota')
async def dota(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали {callback.data}')
    await callback.message.answer('Выбери скин:', reply_markup=kb.dota_k)

@router.callback_query(F.data == 'marci')
async def marci(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали {callback.data}')
    await callback.message.answer_photo(photo='https://sun9-77.userapi.com/impg/nL7PdBzqhaYIo0KLQwPxK5WDb29pG3r6lQfWAQ/NWjnrDOy-iI.jpg?size=1920x1080&quality=96&sign=f8755eeb4cd707bd0c66ca5b28561804&type=album',
                                        caption='Price: 1000rub', reply_markup=kb.buy_dota)

@router.callback_query(F.data == 'snapfire')
async def snapfire(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали {callback.data}')
    await callback.message.answer_photo(photo='https://sun9-54.userapi.com/impg/D5e7ueHKcx8dL_ng1BbRnjpFCj57Y7nZj52nWQ/LEfRJqK-pdo.jpg?size=665x687&quality=96&sign=10c2370d138770a46dfb67f1314efd1b&c_uniq_tag=5s5zpZMM8qp3BheSMMDgr0v7AHairnj2S8B-cUHFNs0&type=album',
                                         caption='Price: 800rub', reply_markup=kb.buy_dota)

@router.callback_query(F.data == 'mirana')
async def mirana(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали {callback.data}')
    await callback.message.answer_photo(photo='https://cdn.oneesports.gg/cdn-data/2021/12/Dota2_Dark_Moon_Mirana_battle_pass_bundle-1024x575.jpg',
                                         caption='Price: 2000rub', reply_markup=kb.buy_dota)

@router.callback_query(F.data == 'kunkka')
async def kunkka(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали {callback.data}')
    await callback.message.answer_photo(photo='https://collectorsshop.ru/img/catalog/items/main_images/2023/08/1400.png',
                                         caption='Price: 500rub', reply_markup=kb.buy_dota)

@router.callback_query(F.data == 'backtodota_k')
async def backtodota_k(callback: CallbackQuery):
    await callback.answer('Клик')
    await callback.message.answer('Назад', reply_markup=kb.catalog)

@router.callback_query(F.data == 'paydota')
async def paydota(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали {callback.data}')
    await callback.message.reply('Связь: @dtqwe')

@router.callback_query(F.data == 'backdota')
async def backdota(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали {callback.data}')
    await callback.message.answer('Назад', reply_markup=kb.dota_k)



@router.callback_query(F.data == 'csgo')
async def csgo(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали {callback.data}')
    await callback.message.answer('Выбери скин:', reply_markup=kb.csgo_k)

@router.callback_query(F.data == 'usp')
async def usp(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали {callback.data}')
    await callback.message.answer_photo(photo='https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpoo6m1FBRp3_bGcjhQ09-jq5WYh8jgPITZk2dd18h0juDU-LP5iUazrl0_Nj_6d9eRcVVrZ1iD_FDvwu3r0J7t6MmbmCRhunEm7XeOyhS-hhtJcKUx0kcRs1rK/360fx360f',
                                        caption='Price: 50rub', reply_markup=kb.buy_csgo)
    
@router.callback_query(F.data == 'ak')
async def ak(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали {callback.data}')
    await callback.message.answer_photo(photo='https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot7HxfDhjxszJemkV09G3h5SOhe7LPr7Vn35c18lwmO7Eu4ih0VDi80drZ276JtfBdQE4ZA3S8gXoxebogZ-57ZiYmCFlvyIi5HjD30vgrWhS6dA/360fx360f',
                                        caption='Price: 150rub', reply_markup=kb.buy_csgo)
    
@router.callback_query(F.data == 'm4')
async def m4(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали {callback.data}')
    await callback.message.answer_photo(photo='https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpou-6kejhnwMzFJTwW09--m5CbkuXLNLPehX9u5cB1g_zMyoD0mlOx5UJpMm_1INSUdQ82YFGErge5w73phMe-7czNyiMw6SUk5i6IzkC3hklSLrs4dv2Dfk0/360fx360f',
                                        caption='Price: 100rub', reply_markup=kb.buy_csgo)

@router.callback_query(F.data == 'awp')
async def awp(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали {callback.data}')
    await callback.message.answer_photo(photo='https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot621FBRw7P7NYjV9-N24q42Ok_7hPoTdl3lW7Yt3iOuRrdT32wPk-UI9YW_xJo_HewJoZwuE8lbryejsh5bv7ZmYmiFjpGB8shCX1QG8/360fx360f',
                                        caption='Price: 100rub', reply_markup=kb.buy_csgo)

@router.callback_query(F.data == 'backtocsgo_k')
async def backtocsgo_k(callback: CallbackQuery):
    await callback.answer('Клик')
    await callback.message.answer('Назад', reply_markup=kb.catalog)
    

@router.callback_query(F.data == 'paycsgo')
async def paycsgo(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали {callback.data}')
    await callback.message.reply('Связь: @dtqwe')

@router.callback_query(F.data == 'backcsgo')
async def backcsgo(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали {callback.data}')
    await callback.message.answer('Назад', reply_markup=kb.csgo_k)

@router.message(F.text == 'Оценка')
async def rate(message: Message):
    user_id = message.from_user.id

    # Проверяем, не поставил ли пользователь оценку ранее
    conn = sqlite3.connect("bot_ratings.db")
    cursor = conn.cursor()
    cursor.execute("SELECT rate FROM ratings WHERE user_id = ?", (user_id,))
    previous_rating = cursor.fetchone()
    conn.close()

    if previous_rating:
        await message.answer('Вы уже поставили оценку боту ранее.')
    else:
        await message.answer('Пожалуйста, оставьте оценку боту!', reply_markup=kb.rate)


@router.callback_query(F.data == 'rate1')
async def rate1(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали {callback.data}')
    user_id = callback.from_user.id
    username = callback.from_user.username
    rating = 1  # Низкая оценка

    # Запишем оценку в базу данных
    conn = sqlite3.connect("bot_ratings.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ratings (user_id, username, date, rate) VALUES (?, ?, ?, ?)",
                   (user_id, username, datetime.datetime.now(), rating))
    conn.commit()
    conn.close()

    await callback.message.answer('Спасибо за оценку!')

@router.callback_query(F.data == 'rate2')
async def rate2(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали {callback.data}')
    user_id = callback.from_user.id
    username = callback.from_user.username
    rating = 2

    # Запишем оценку в базу данных
    conn = sqlite3.connect("bot_ratings.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ratings (user_id, username, date, rate) VALUES (?, ?, ?, ?)",
                   (user_id, username, datetime.datetime.now(), rating))
    conn.commit()
    conn.close()

    await callback.message.answer('Спасибо за оценку!')

@router.callback_query(F.data == 'rate3')
async def rate3(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали {callback.data}')
    user_id = callback.from_user.id
    username = callback.from_user.username
    rating = 3

    # Запишем оценку в базу данных
    conn = sqlite3.connect("bot_ratings.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ratings (user_id, username, date, rate) VALUES (?, ?, ?, ?)",
                   (user_id, username, datetime.datetime.now(), rating))
    conn.commit()
    conn.close()

    await callback.message.answer('Спасибо за оценку!')

@router.callback_query(F.data == 'rate4')
async def rate4(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали {callback.data}')
    user_id = callback.from_user.id
    username = callback.from_user.username
    rating = 4

    # Запишем оценку в базу данных
    conn = sqlite3.connect("bot_ratings.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ratings (user_id, username, date, rate) VALUES (?, ?, ?, ?)",
                   (user_id, username, datetime.datetime.now(), rating))
    conn.commit()
    conn.close()

    await callback.message.answer('Спасибо за оценку!')

@router.callback_query(F.data == 'rate5')
async def rate5(callback: CallbackQuery):
    await callback.answer(f'Вы выбрали {callback.data}')
    user_id = callback.from_user.id
    username = callback.from_user.username
    rating = 5

    # Запишем оценку в базу данных
    conn = sqlite3.connect("bot_ratings.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ratings (user_id, username, date, rate) VALUES (?, ?, ?, ?)",
                   (user_id, username, datetime.datetime.now(), rating))
    conn.commit()
    conn.close()

    await callback.message.answer('Спасибо за оценку!')



@router.message(F.text == 'Профиль')
async def profile(message: Message):
    user_id = message.from_user.id
    conn = sqlite3.connect("bot_ratings.db")
    cursor = conn.cursor()

    # Получаем оценку пользователя из базы данных
    cursor.execute("SELECT rate FROM ratings WHERE user_id = ?", (user_id,))
    user_rating = cursor.fetchone()

    if user_rating:
        await message.answer(f'Ваш ID: {user_id}\nЛогин: {message.from_user.first_name}\nОценка боту: {user_rating[0]}')
    else:
        await message.answer(f'Ваш ID: {user_id}\nЛогин: {message.from_user.first_name}\nОценка боту: нету')

    conn.close()


@router.message(F.text == 'Контакты')
async def contact(message: Message):
    await message.answer('👤Менеджер: @dtqwe')