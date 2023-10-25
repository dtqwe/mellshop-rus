from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)


main_kb = [
    [KeyboardButton(text='Каталог'),
     KeyboardButton(text='Профиль')],
     [KeyboardButton(text='Оценка'),
     KeyboardButton(text='Контакты')]
]

main = ReplyKeyboardMarkup(keyboard=main_kb, resize_keyboard=True, input_field_placeholder='Выберите пункт ниже')


socials_kb = [
    [InlineKeyboardButton(text='Telegram', url='https://t.me/dtqwe')]
]

socials = InlineKeyboardMarkup(inline_keyboard=socials_kb)

rate = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1', callback_data='rate1')],
    [InlineKeyboardButton(text='2', callback_data='rate2')],
    [InlineKeyboardButton(text='3', callback_data='rate3')],
    [InlineKeyboardButton(text='4', callback_data='rate4')],
    [InlineKeyboardButton(text='5', callback_data='rate5')]
])


catalog = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Dota2', callback_data='dota')],
    [InlineKeyboardButton(text='CS:GO', callback_data='csgo')]
])

dota_k = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Marci | Brightfist', callback_data='marci')],
    [InlineKeyboardButton(text='Snapfire | Snailfire', callback_data='snapfire')],
    [InlineKeyboardButton(text='Mirana of Nightsilver', callback_data='mirana')],
    [InlineKeyboardButton(text='Kunkka | Sea Spirit', callback_data='kunkka')],
    [InlineKeyboardButton(text='Назад', callback_data='backtodota_k')]    
])

csgo_k = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='USP-S | Билет в ад', callback_data='usp')],
    [InlineKeyboardButton(text='AK-47 | Элитное снаряжение', callback_data='ak')],
    [InlineKeyboardButton(text='StatTrak™ M4A4 | Магний', callback_data='m4')],
    [InlineKeyboardButton(text='AWP | Африканская сетка', callback_data='awp')],
    [InlineKeyboardButton(text='Назад', callback_data='backtocsgo_k')]
])

buy_dota = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Купить', callback_data='paydota')],
    [InlineKeyboardButton(text='Назад', callback_data='backdota')]
])

buy_csgo = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Купить', callback_data='paycsgo')],
    [InlineKeyboardButton(text='Назад', callback_data='backcsgo')]
])