from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


shipping_kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('Самовывоз')
b2 = KeyboardButton('Доставка на дом')

shipping_kb.row(b1, b2)