from aiogram import types, Dispatcher
from datetime import datetime
from keyboards import client_keyboard


async def start_command(message: types.Message):
    try:
        await message.bot.send_message(message.from_user.id, 'Study Bot by mmagistr. '
                                                             'Use your keyboard.', reply_markup=client_keyboard)
        await message.delete()
    except:
        await message.reply('type something to bot: https://web.telegram.org/a/#6075314190')


async def client_command(message: types.Message):
    await message.bot.send_message(message.from_user.id, 'u are just client')
    await message.delete()


async def time_command(message: types.Message):
    await message.answer(f'Time is {datetime.now().strftime("%H:%M")}')
    await message.delete()


async def institute_command(message: types.Message):
    await message.answer(f'Good institutes: ТюмГУ, УРФУ.')
    await message.delete()


async def about_me_command(message: types.Message):
    now = datetime.now()
    born = datetime(year=2023, month=7, day=20)
    delta = now - born
    await message.answer(f'Telegram bot, was architect by mmagistr. I am live {delta.days} days')
    await message.delete()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(client_command, commands=['client'])
    dp.register_message_handler(time_command, commands=['time'])
    dp.register_message_handler(institute_command, commands=['institutes'])
    dp.register_message_handler(about_me_command, commands=['about'])
    dp.register_message_handler(start_command, commands=['start', 'help'])
