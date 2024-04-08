from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


start_kb = ReplyKeyboardMarkup(resize_keyboard=True)

order_btn = KeyboardButton('/заказать')
show_cakes_btn = KeyboardButton('/показать_торты')
info_btn = KeyboardButton('/информация')
login_btn = KeyboardButton('/администратор')

start_kb.row(order_btn, info_btn, show_cakes_btn).row(login_btn)