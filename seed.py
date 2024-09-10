from datetime import datetime
import faker
from random import randint, choice
import sqlite3

NUMBER_USERS = 20
NUMBER_TASKS = 100

def generate_fake_data(number_users, number_tasks) -> tuple():
    fake_names = []# тут зберігатимемо імена користувачів
    fake_emails = []# тут зберігатимемо поштові скриньки користувачів
    fake_titles = []# тут зберігатимемо назви завдань
    fake_descr = []# тут зберігаємо описи завдань
    '''Візьмемо три компанії з faker і помістимо їх у потрібну змінну'''
    fake_data = faker.Faker()

# Створимо набір користувачів у кількості NUMBER_USERS
    for _ in range(number_users):
        fake_names.append(fake_data.name())
        fake_emails.append(fake_data.email())

# Створимо набір завдань у кількості NUMBER_TASKS
    for _ in range(number_tasks):
        fake_titles.append(fake_data.text(100))
        fake_descr.append(fake_data.text())

    return fake_names, fake_emails, fake_titles, fake_descr


def prepare_data(names, emails, titles, descr) -> tuple():

    for_users = []
    # готуємо список кортежів з іменами та електронними поштами
    for user, email in zip(names, emails):
        for_users.append((user, email))

    for_tasks = []
    # готуємо список кортежів з назвами та описом завданнь, також зі статусами та до якого користувача відноситься
    for title, desc in zip(titles, descr):
        for_tasks.append((title, desc, randint(1, 3), randint(1, NUMBER_USERS)))

    return for_users, for_tasks

def insert_data_to_db(users, tasks) -> None:
# Створимо з'єднання з нашою БД та отримаємо об'єкт курсора для маніпуляцій з даними

    with sqlite3.connect('hw02.db') as con:

        cur = con.cursor()

# заповнюємо таблицю зі значеннями у таблиці статусів
        statuses = [('new',), ('in progress',), ('completed',)]
        sql_to_status = """INSERT INTO status(name)
                                VALUES (?)"""
        try:
            cur.executemany(sql_to_status, statuses)
        except:
            pass

# заповнюємо таблицю з користувачами
        sql_to_users = """INSERT INTO users(fullname, email)
                               VALUES (?, ?)"""

        cur.executemany(sql_to_users, users)

# заповнюємо таблицю з завданнями
        sql_to_tasks = """INSERT INTO tasks(title, description, status_id, user_id)
                              VALUES (?, ?, ?, ?)"""

        cur.executemany(sql_to_tasks, tasks)

# Фіксуємо наші зміни в БД

        con.commit()

if __name__ == "__main__":
    users, tasks = prepare_data(*generate_fake_data(NUMBER_USERS, NUMBER_TASKS))
    insert_data_to_db(users, tasks)

