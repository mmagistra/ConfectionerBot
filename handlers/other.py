from aiogram import types, Dispatcher


async def other_command(message: types.Message):
    await message.bot.send_message(message.from_user.id, 'other command')
    await message.delete()


async def start(message: types.Message):
    await message.bot.send_message(message.from_user.id, "Hi, I'm study bot! I have some functions"
                                                         ", but i try do more!")
    await message.delete()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(other_command, commands=['other'])
