from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('/администратор')
b2 = KeyboardButton('/показать_администраторов')
b3 = KeyboardButton('/удалить_администратора')
b4 = KeyboardButton('/поменять_пароль')
b5 = KeyboardButton('/показать_пароль')
b6 = KeyboardButton('/добавить_торт')
b7 = KeyboardButton('/показать_торты')
b8 = KeyboardButton('/удалить_торт')
b9 = KeyboardButton('/информация')

admin_panel.row(b1).row(b2, b3).row(b5, b4).row(b6, b7, b8).row(b9)
