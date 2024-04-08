from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


confirm_weight_kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('Да, продолжить')
b2 = KeyboardButton('Нет, ввести другой текст')

confirm_weight_kb.row(b1, b2)