from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('/login')
b2 = KeyboardButton('/show_admins')
b3 = KeyboardButton('/delete_admin')
b4 = KeyboardButton('/change_password')
b5 = KeyboardButton('/show_password')
b6 = KeyboardButton('/add_cake')
b7 = KeyboardButton('show_cakes')
b8 = KeyboardButton('/delete_cake')
b9 = KeyboardButton('/info')

admin_panel.row(b1).row(b2, b3).row(b4, b5).row(b6, b7, b8).row(b9)