from aiogram import executor
from create_bot import dp
from handlers import cliant, admin, other
from data_base.postgresql import sql_start

print('start bot')
sql_start()


cliant.register_handlers_client(dp)


if __name__ == '__main__':
    executor.start_polling(dp)
