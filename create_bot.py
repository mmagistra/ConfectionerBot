from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db.sqlite_db_worker import DbWorker


with open('./local_debug/token.txt') as f:
    TOKEN = f.read()

storage = MemoryStorage()

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)
db_worker = DbWorker()
