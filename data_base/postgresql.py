import psycopg2
from create_bot import bot


def sql_start():
    global conn, cur
    conn = psycopg2.connect(database="finans",
                            user="andrii",
                            password="sql",
                            host="127.0.0.1",
                            port="5432")
    cur = conn.cursor()

    if conn:
        print('База данных работает')

    cur.execute('CREATE TABLE IF NOT EXISTS bekommen(wievile INT, currency TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS geben(tehem TEXT, wievil INT, currenc TEXT)')
    conn.commit()


async def sql_add_command(state):
    async with state.proxy() as date:
        cur.execute('INSERT INTO bekommen (wievile, currency) VALUES (%s, %s)', (date['wievile'], date['currency']))
        conn.commit()


async def sql_read(message):
    cur.execute("SELECT * FROM bekommen WHERE currency=%s", ('$',))
    usd_numbers = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT * FROM bekommen WHERE currency=%s", ('€',))
    eur_numbers = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT * FROM bekommen WHERE currency=%s", ('UAH',))
    uah_numbers = [row[0] for row in cur.fetchall()]
    conn.close()
    total_usd = sum(usd_numbers)
    total_eur = sum(eur_numbers)
    total_uah = sum(uah_numbers)
    await bot.send_message(message.from_user.id, f"Общяя сумма заработаного от дохода {total_usd}$")
    await bot.send_message(message.from_user.id, f"Общяя сумма заработаного от дохода {total_eur}€")
    await bot.send_message(message.from_user.id, f"Общяя сумма заработаного от дохода {total_uah}грн")


async def sql_add_command_de(state):
    async with state.proxy() as deta:
        cur.execute('INSERT INTO geben (tehem, wievil, currenc) VALUES (%s, %s, %s)',
                    (deta['tehem'], deta['wievil'], deta['currenc']))
        conn.commit()


async def sql_read_min(message):
    cur = conn.cursor()
    cur.execute("SELECT tehem, SUM(wievil) FROM geben GROUP BY tehem")
    category_totals = cur.fetchall()
    conn.close()
    for category, total in category_totals:
        await bot.send_message(message.from_user.id, f"Общая сумма потраченного для категории '{category}': {total}")


async def get_total_balance(message):
    cur.execute("SELECT SUM(wievile) FROM bekommen WHERE currency=%s", ('$',))
    total_income_base_usa = cur.fetchone()[0] or 0
    cur.execute("SELECT SUM(wievile) FROM bekommen WHERE currency=%s", ('€',))
    total_income_base_eur = cur.fetchone()[0] or 0
    cur.execute("SELECT SUM(wievile) FROM bekommen WHERE currency=%s", ('UAH',))
    total_income_base_uah = cur.fetchone()[0] or 0

    cur.execute("SELECT SUM(wievil) FROM geben WHERE currenc=%s", ('$',))
    total_expenses_base_usa = cur.fetchone()[0] or 0
    cur.execute("SELECT SUM(wievil) FROM geben WHERE currenc=%s", ('€',))
    total_expenses_base_eur = cur.fetchone()[0] or 0
    cur.execute("SELECT SUM(wievil) FROM geben WHERE currenc=%s", ('UAH',))
    total_expenses_base_uah = cur.fetchone()[0] or 0

    total_balance_usa = total_income_base_usa - total_expenses_base_usa
    total_balance_eur = total_income_base_eur - total_expenses_base_eur
    total_balance_uah = total_income_base_uah - total_expenses_base_uah
    await bot.send_message(message.from_user.id, f"Ваш текущий баланс в {total_balance_usa}$")
    await bot.send_message(message.from_user.id, f"Ваш текущий баланс в {total_balance_eur}€")
    await bot.send_message(message.from_user.id, f"Ваш текущий баланс в {total_balance_uah}грн")


async def sql_clear_data(message):
    cur.execute('DELETE FROM bekommen')
    cur.execute('DELETE FROM geben')
    conn.commit()
    await bot.send_message(message.from_user.id, f"Очистка данных произошла")
