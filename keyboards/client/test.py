from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


test_kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('some text...')
b2 = KeyboardButton('some text...')
b3 = KeyboardButton('some text...')
b4 = KeyboardButton('some text...')

test_kb.row(b1, b2).row(b3, b4)
