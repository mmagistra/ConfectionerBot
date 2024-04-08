from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


accept_kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('Оставить')
b2 = KeyboardButton('Изменить')

accept_kb.row(b1, b2)
