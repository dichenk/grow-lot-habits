import datetime
from datetime import timedelta

import pandas as pd
import requests
from decouple import config
import psycopg2

TOKEN = config('TELE_TOKEN')


def read_db(tg_id, email):  # записывает в бд telegram id, чтобы рассылать уведомления
    sql = f"UPDATE app_custom_user_customuser SET tg_id = \'{tg_id}\' WHERE email = \'{email}\'"
    try:
        conn = psycopg2.connect(
            database="tele_habit",
            host="localhost",
            user="oleg",
            password="12345",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except:
        print('error')


def send_tg(chat_id, SEND_MESSAGE = 'post'):  # напоминалка тем, кто обратился к боту, но не скинул свой email
    if SEND_MESSAGE == 'post':
        SEND_MESSAGE = 'Какая у вас почта? Укажите для получения уведомлений в телеграм.'
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={SEND_MESSAGE}"
    requests.get(url)


def read_tg():
    URL_GET_ID = f"https://api.telegram.org/bot{TOKEN}/getUpdates"  # получаем обновления (кто вызывал бота)
    for i in requests.get(URL_GET_ID).json()['result']:
        tg_id = i['message']['from']['id']
        tg_entities = i['message'].get('entities')
        if tg_entities:
            tg_entities = tg_entities[0]
            if tg_entities['type'] == 'bot_command' and check_id(tg_id):  # если к боту обратились, а email еще не предоставляли - напомним о себе
                send_tg(tg_id)
            if tg_entities['type'] == 'email':  #  если боту отправили email, запишем его в бд
                read_db(tg_id, i['message']['text'])


def check_id(tg_id):  # проверяет, записан ли telegram id в нашу базу
    sql = f"SELECT * FROM app_custom_user_customuser WHERE tg_id = \'{tg_id}\'"
    try:
        conn = psycopg2.connect(
            database="tele_habit",
            host="localhost",
            user="oleg",
            password="12345",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute(sql)
        # print(cur)
        cur.close()
    except:
        print('error')


def make_notification():
    sql_update = f"UPDATE app_habit_habit SET date_notification=CURRENT_DATE+1 WHERE date_notification is null and time<CURRENT_TIME" # установим дату уведомления для новых привычек - завтра, если время уже прошло
    sql_update2 = f"UPDATE app_habit_habit SET date_notification=CURRENT_DATE WHERE date_notification is null and time>=CURRENT_TIME" # установим дату уведомления для новых привычек - сегодня, если время еще не прошло
    sql_read = f"SELECT * FROM app_habit_habit INNER JOIN app_custom_user_customuser ON app_custom_user_customuser.id = app_habit_habit.author_id WHERE date_notification=CURRENT_DATE and time<=CURRENT_TIME" # читаем бд, чтобы провести напоминания через tg
    sql_update3 = f"UPDATE app_habit_habit SET date_notification=CURRENT_DATE+periodic_habit WHERE date_notification=CURRENT_DATE and time<=CURRENT_TIME" # меняем дату уведомления (в соответствии с периодичностью) для всех, кому разослали уведомления
    try:
        conn = psycopg2.connect(
            database="tele_habit",
            host="localhost",
            user="oleg",
            password="12345",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute(sql_update)
        cur.execute(sql_update2)
        conn.commit()
        cur.execute(sql_read)
        data = cur.fetchall()
        df = pd.DataFrame(data=data)
        for i in range(len(df)):  # отправляем уведомления в тг
            send_tg(df.at[i, 26], df.at[i,5])
        cur.execute(sql_update3)
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print('error', error)
    finally:
        if conn:
            cur.close()
            conn.close()



# read_tg()  # проверяем работу функций
# make_notification()