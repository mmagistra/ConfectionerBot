from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

description_type_kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('Добавить только изображение')
b2 = KeyboardButton('Добавить только текст')
b3 = KeyboardButton('Добавить изображение и текст')
b4 = KeyboardButton('Не добавлять пожелания')

description_type_kb.row(b1, b2, b3).row(b4)
