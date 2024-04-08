from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram import Dispatcher


from keyboards.other.start import start_kb


async def empty(message: Message):
    await message.answer('Я Вас не понимаю :(. Используйте команду /help, чтобы разобраться что к чему',
                         reply_markup=start_kb)


def register_other_handlers(dp: Dispatcher):
    dp.register_message_handler(empty)
