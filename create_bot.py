from aiogram import Bot, Dispatcher, types
from TOKEN import telegram_token
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token=telegram_token, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
