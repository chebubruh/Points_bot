from psycopg2 import *
import config
from datetime import *

subjects = ['Общетеоретические_дисциплины',
            'Цивилистические_дисциплины',
            'Земельное_право',
            'Природоресурсное_право',
            'Предпринимательское_право',
            'Судебное_делопроизводство',
            'СудебноЭкспертная_деятельность']


def show_date():  # возвращает сегодняшнюю дату
    day = date.today().day
    month = date.today().month
    year = date.today().year
    return f'{day}.{month}.{year}'


def add_date(name_subjects):  # заносит сегодняшнюю дату в таблицу
    with connect(user=config.user, password=config.password, host=config.host, database=config.database,
                 port=config.port) as db:
        cur = db.cursor()
        cur.execute(f"SELECT date FROM {name_subjects}")
        a = cur.fetchall()
        if show_date() not in str(a):
            cur.execute(f"INSERT INTO {name_subjects} (date) VALUES ('{show_date()}')")


def create_students(name):  # заносит студента в таблицу
    with connect(user=config.user, password=config.password, host=config.host, database=config.database,
                 port=config.port) as db:
        cur = db.cursor()
        for i in subjects:
            cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{i}'")
            a = cur.fetchall()
            if name not in str(a):
                cur.execute(f"ALTER TABLE {i} ADD COLUMN {name} TEXT")


def add_points(name_subjects, name, form):  # заносит баллы в таблицу
    add_date(name_subjects)
    with connect(user=config.user, password=config.password, host=config.host, database=config.database,
                 port=config.port) as db:
        cur = db.cursor()
        cur.execute(f"SELECT {name} FROM {name_subjects} WHERE date = '{show_date()}'")
        a = cur.fetchall()
        if form == True:
            if a[0][0] == None:
                cur.execute(f"UPDATE {name_subjects} SET {name} = 1 WHERE date = '{show_date()}'")
            elif a[0][0] == '1' or a[0][0] == 'д+1' or a[0][0] == '1+д' or a[0][0] == '1+д+д' or a[0][0] == 'д+д+1' or \
                    a[0][0] == 'д+1+д':
                return 'кого ты обманываешь? товой максимум - это 1 ответ за семинар'
            elif a[0][0] == 'д' or a[0][0] == 'д+д':
                cur.execute(f"UPDATE {name_subjects} SET {name} = '{a[0][0]}+1' WHERE date = '{show_date()}'")

        elif form == False:
            if a[0][0] == None:
                cur.execute(f"UPDATE {name_subjects} SET {name} = 'д' WHERE date = '{show_date()}'")
            elif a[0][0] == '1' or a[0][0] == 'д':
                cur.execute(f"UPDATE {name_subjects} SET {name} = '{a[0][0]}+д' WHERE date = '{show_date()}'")
            elif a[0][0] == '1+д' or a[0][0] == 'д+1':
                cur.execute(f"UPDATE {name_subjects} SET {name} = '{a[0][0]}+д' WHERE date = '{show_date()}'")


def total_points(name_subjects, name):  # подсчитывает ответы
    answers = 0
    dlc = 0
    with connect(user=config.user, password=config.password, host=config.host, database=config.database,
                 port=config.port) as db:
        cur = db.cursor()
        cur.execute(f"SELECT {name} FROM {name_subjects}")
        a = cur.fetchall()
        for i in a:
            for j in i:
                if j == None:
                    continue
                else:
                    answers += j.count('1')
                    dlc += j.count('д')
    return f'Предмет: {name_subjects}\nОтветы: {answers}\nДополнения: {dlc}'


def clear(name):  # удаляет все баллы, полученные в этот день
    with connect(user=config.user, password=config.password, host=config.host, database=config.database,
                 port=config.port) as db:
        cur = db.cursor()
        for i in subjects:
            cur.execute(f"DELETE FROM {i} WHERE {name} IS NOT NULL AND date = '{show_date()}'")


def view_table(name_subjects, name):  # возвращает всю таблицу для конкретного человека
    table = f'{name_subjects}\n\n'

    with connect(user=config.user, password=config.password, host=config.host, database=config.database,
                 port=config.port) as db:
        cur = db.cursor()
        cur.execute(f"SELECT date, {name} FROM {name_subjects}")
        a = cur.fetchall()
        for i in a:
            table += f'{i[0]} - {i[1]}\n'

    return table


def all_points(name):  # возвращает сводку баллов по всем предметам
    result = 'ОТВЕТЫ / ДОПОЛНЕНИЯ\n\n'
    with connect(user=config.user, password=config.password, host=config.host, database=config.database,
                 port=config.port) as db:
        for b in subjects:
            answers = 0
            dlc = 0
            cur = db.cursor()
            cur.execute(f"SELECT {name} FROM {b}")
            a = cur.fetchall()
            for i in a:
                for j in i:
                    if j == None:
                        continue
                    else:
                        answers += j.count('1')
                        dlc += j.count('д')
            result += f'{b}: {answers} / {dlc}\n'
    return result

# СОЗДАНИЕ -----------------------------

# with connect(user=config.user, password=config.password, host=config.host, database=config.database, port=config.port) as db:
#     cur = db.cursor()
#     for i in subjects:
#         cur.execute(f"""CREATE TABLE {i} (
#                 date TEXT
#                 )""")
# СОЗДАНИЕ -----------------------------


# УДАЛЕНИЕ -----------------------------

# with connect(user=config.user, password=config.password, host=config.host, database=config.database, port=config.port) as db:
#     cur = db.cursor()
#     for i in subjects:
#         cur.execute(f"DELETE FROM {i}")

# УДАЛЕНИЕ -----------------------------
