from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from conf import BOT_API

bot = Bot(token=BOT_API)
dp  = Dispatcher(bot, storage=MemoryStorage())
