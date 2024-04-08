from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


package_kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('Хочу')
b2 = KeyboardButton('Спасибо, не нужна')

package_kb.row(b1, b2)