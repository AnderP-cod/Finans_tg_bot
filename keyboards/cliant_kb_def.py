from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('/Заработал')
b2 = KeyboardButton('/Потратил')
b3 = KeyboardButton('/Таблица_заработаного')
b4 = KeyboardButton('/Таблица_потрачиного')
b5 = KeyboardButton('/Общяя_сумма_денег')
b6 = KeyboardButton('/Очистить_все_данные!!!!!')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).add(b2).add(b3).add(b4).add(b5).add(b6)

b1 = KeyboardButton('Food')
b2 = KeyboardButton('Technique')
b3 = KeyboardButton('Present')
b4 = KeyboardButton('McDonalds')
b5 = KeyboardButton('Others')

in_client = ReplyKeyboardMarkup(resize_keyboard=True)

in_client.add(b1).add(b2).add(b3).add(b4).add(b5)


b1 = KeyboardButton('$')
b2 = KeyboardButton('€')
b3 = KeyboardButton('UAH')

cu_client = ReplyKeyboardMarkup(resize_keyboard=True)

cu_client.add(b1).add(b2).add(b3)
