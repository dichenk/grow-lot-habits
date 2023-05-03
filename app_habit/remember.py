import pandas as pd
import sqlite3
import requests
from decouple import config
import psycopg2

TOKEN = config('TELE_TOKEN')


def read_db(tg_id, email):
    # con = sqlite3.connect('../db.sqlite3')
    # cur = con.cursor()
    # cur.execute(f'')
    # a = cur.fetchall()
    # con.close
    # print(a)
    sql = f"UPDATE app_custom_user_customuser SET tg_id = \'{tg_id}\' WHERE email = \'{email}\'"
    # cursor.fetchall()
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
        print('nice')
    except:
        print('error')




def send_tg(chat_id):
    SEND_MESSAGE = 'Какая у вас почта? Укажите для получения уведомлений в телеграм.'
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={SEND_MESSAGE}"
    print(requests.get(url).json()['result'])  # this sends the message

def read_tg():
    # TOKEN = config('TELE_TOKEN')
    URL_GET_ID = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

    # answer = pd.read_json(requests.get(URL_GET_ID).json()['result'])  # this sends the message
    # print(answer)
    # print(requests.get(URL_GET_ID).json())
    # print(requests.get(URL_GET_ID).json())
    tg_answers = {}
    for i in requests.get(URL_GET_ID).json()['result']:
        print(i)
        tg_id = i['message']['from']['id']
        tg_entities = i['message'].get('entities')
        answer_type = None
        if tg_entities:
            tg_entities = tg_entities[0]
            if tg_entities['type'] == 'bot_command' and not tg_answers.get(tg_id):
                send_tg(tg_id)
            if tg_entities['type'] == 'email':
                print(f'try to write id to db')
                print(tg_id)
                print(i['message']['text'])
                read_db(tg_id, i['message']['text'])

read_tg()

def read_json(variable):  # json.loads не хочет читать одинарные кавычки и True. Поправим.
    variable = variable.replace("'", "\"")
    variable = variable.replace("True", "\"True\"")
    variable = variable.replace("False", "\"False\"")
    variable = json.loads(variable)
    return variable