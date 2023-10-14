from aiogram import types, Dispatcher
from create_bot import dp, bot
from data_base.postgresql import sql_read, sql_read_min, get_total_balance, sql_clear_data
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from data_base.postgresql import sql_add_command, sql_add_command_de
from keyboards.cliant_kb_def import kb_client, in_client, cu_client


class FSMPlusfi(StatesGroup):
    wievile = State()
    currency = State()


class FSMPlusmin(StatesGroup):
    tehem = State()
    wievil = State()
    currenc = State()


async def command_start(message : types.Message):
    await bot.send_message(message.from_user.id,
                           "Телеграм бот, для финансов. Куда вы хотите заполнить свои финансы", reply_markup=kb_client)


async def wievile_bot(message : types.Message):
    await FSMPlusfi.wievile.set()
    await message.reply('Сколько вы заработали')


async def bekommen_bot(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['wievile'] = message.text
    await FSMPlusfi.next()
    await message.reply('В какой валюти вы заработали', reply_markup=cu_client)


async def currency_bot(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['currency'] = message.text
    await sql_add_command(state)
    await state.finish()


async def table_bekommen(message: types.Message):
    await sql_read(message)


async def wievil_bot(message : types.Message):
    await FSMPlusmin.tehem.set()
    await message.reply('Куда вы потратили', reply_markup=in_client)


async def them_bot(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tehem'] = message.text
    await FSMPlusmin.next()
    await message.reply('Сколько вы потратили')


async def bekomme_bot(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['wievil'] = message.text
    await FSMPlusmin.next()
    await message.reply('В какой валюти вы потратили', reply_markup=cu_client)


async def currenc_bot(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['currenc'] = message.text
    await sql_add_command_de(state)
    await state.finish()


async def table_geben(message: types.Message):
    await sql_read_min(message)


async def table_geld(message: types.Message):
    await get_total_balance(message)


async def table_clear(message: types.Message):
    await sql_clear_data(message)


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(wievile_bot, commands=['Заработал'])
    dp.register_message_handler(bekommen_bot, state=FSMPlusfi.wievile)
    dp.register_message_handler(currency_bot, state=FSMPlusfi.currency)
    dp.register_message_handler(table_bekommen, commands=['Таблица_заработаного'])

    dp.register_message_handler(wievil_bot, commands=['Потратил'])
    dp.register_message_handler(them_bot, state=FSMPlusmin.tehem)
    dp.register_message_handler(bekomme_bot, state=FSMPlusmin.wievil)
    dp.register_message_handler(currenc_bot, state=FSMPlusmin.currenc)
    dp.register_message_handler(table_geben, commands=['Таблица_потрачиного'])

    dp.register_message_handler(table_geld, commands=['Общяя_сумма_денег'])
    dp.register_message_handler(table_clear, commands=['Очистить_все_данные!!!!!'])
