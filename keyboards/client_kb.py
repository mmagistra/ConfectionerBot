from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


client_command_button = KeyboardButton('/client')
time_command_button = KeyboardButton('/time')
institute_command_button = KeyboardButton('/institutes')
about_command_button = KeyboardButton('/about')
menu_command_button = KeyboardButton('/menu')

client_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
client_keyboard.row(client_command_button).\
    row(time_command_button, about_command_button).\
    row(institute_command_button).\
    row(menu_command_button)
