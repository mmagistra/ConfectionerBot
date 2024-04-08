from create_bot import dp, db_worker
from aiogram import executor

from handlers.other import register_other_handlers
from handlers.client import register_client_handlers
from handlers.admin import register_admin_handlers

import logging


logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    await db_worker.connect('confectioner_bot_db.db')
    print('db_connected')
    print('bot is online')


async def on_shutdown(_):
    await db_worker.shutdown()


register_client_handlers(dp)  # first registration!
register_admin_handlers(dp)  # second registration!
register_other_handlers(dp)  # third registration!


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
