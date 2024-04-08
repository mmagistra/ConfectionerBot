from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


request_contact_kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(text="Отправить номер телефона 📱", request_contact=True)

request_contact_kb.add(b1)
