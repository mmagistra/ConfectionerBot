from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


weight_kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('1 кг')
b2 = KeyboardButton('2 кг')
b3 = KeyboardButton('3 кг')
b4 = KeyboardButton('4 кг')
b5 = KeyboardButton('5 кг')

weight_kb.row(b1, b2).row(b3, b4, b5)