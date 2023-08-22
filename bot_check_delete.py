import base64
from io import BytesIO
from pathlib import Path

import telebot
from telebot.types import Message, ReplyKeyboardMarkup
from config import Token
import sqlite3
from datetime import datetime
from telebot import types
from emoji import emojize
import re
from urllib.request import urlopen
import random, string

TOKEN = 'YOUR TOKEN'
ADMIN_ID = 'ADMIN_ID'
user = []
bot = telebot.TeleBot(TOKEN)

iterat = 1

class data_temp:
    def __init__(self):
        self.userid = ''
        self.time_sent = ''
        self.size = ''
        self.user = []
        self.price = 0
        self.cart = []

    def clear(self):
        self.userid = ''
        self.time_sent = ''
        self.size = ''
        self.user = []
        self.price = 0
        self.cart = []


def init_table():
    try:
        conn = sqlite3.connect('orders.db')
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS orders(
       userid TEXT NOT NULL,
       name TEXT,
       time_sent TEXT NOT NULL,
       model TEXT,
       size TEXT);
       """)
        conn.commit()
    except:
        print('AMOGUS')

    try:
        conn = sqlite3.connect('orders.db')
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS legiters(
               userid TEXT NOT NULL,
               chatid TEXT NOT NULL,
               name TEXT,
               time_subscr TEXT NOT NULL,
               subscr_duration TEXT);
               """)
        conn.commit()
    except:
        print('AMOGUS')

    try:
        conn = sqlite3.connect('orders.db')
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS legit_orders(
               userid TEXT,
               chatid TEXT,
               photo BLOB,
               link TEXT,
               time_sent TEXT);
               """)
        conn.commit()
    except:
        print('AMOGUS')



conn = sqlite3.connect('orders.db')
cur = conn.cursor()


@bot.message_handler(commands=['start'])
def start_message(message):
    data_t = data_temp()

    name = message.from_user.first_name
    username = message.from_user.username
    time_message_sent = datetime.now()
    data_t.user = [username, time_message_sent]
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text= 'Сделать заказ', callback_data="frm1")
    btn2 = types.InlineKeyboardButton(text= 'Мои заказы', callback_data='ordlst')
    btn3 = types.InlineKeyboardButton(text='О нас', callback_data='about')
    btn4 = types.InlineKeyboardButton(text='Легит-чек', callback_data='legit')
    btn5 = types.InlineKeyboardButton(text='Отзывы', url='https://t.me/POIZON_ORDERING_FEEDBACK')
    kb.row(btn1, btn2)
    kb.row(btn4)
    kb.row(btn3, btn5)
    # kb.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_photo(message.chat.id, 'https://i.imgur.com/FAgqO51.jpg', caption="Привет! Это бот для заказов с POIZON S2P.", reply_markup=kb)

    # formnull(message)


@bot.callback_query_handler(func=lambda call: call.data == "about")
def about_us(callback):
    msg = f'Мы предоставляем услуги по заказу любых товаров с площадки POIZON.\nС нами ваша жизнь станет чуточку удобнее'
    bot.send_message(chat_id=callback.message.chat.id, text=msg)


@bot.callback_query_handler(func=lambda call: call.data == "ordlst")
def order_list(callback):
    bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id - 1)
    # print(callback)
    try:
        conn = sqlite3.connect('orders.db')
        cur = conn.cursor()
        sql_select_query = """SELECT time_sent, model, size, price, F_I_O, order_type, phone_number, photo_check from orders where userid = ?"""
        cur.execute(sql_select_query, (callback.from_user.username, ))
        data = cur.fetchall()
        if len(data) != 0:

            for i in range(len(data)):
                msg = f'Время: {data[i][0]}\n\nСсылка на товар: {data[i][1]}\n\nРазмер товара: {data[i][2]}\n\n Цена товара в ¥: {data[i][3]}\n\nФИО: {data[i][4]}\n\nВид выдачи заказа: {data[i][5]}\n\nНомер телефона: {data[i][6]}'
                with open("files/imageToSave.jpg", "wb") as fh:
                    fh.write(base64.decodebytes(data[i][7]))
                    bot.send_photo(callback.message.chat.id, open("files/imageToSave.jpg", "rb"), caption=msg)

        else:
            bot.send_message(callback.message.chat.id, 'У вас еще нету заказов!')

    except Exception as error:
        print(error)


@bot.callback_query_handler(func=lambda call: call.data == "legit")
def legit_check(callback):
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='gottaluvlnvv', callback_data="form_legit_data_collect_gottaluvlnv")
    btn2 = types.InlineKeyboardButton(text='roysmort', callback_data="form_legit_data_collect_roysmort")
    kb.row(btn1)
    kb.row(btn2)
    bot.send_message(callback.message.chat.id, 'Выберите легитера из каталога', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data == "form_legit_data_collect_gottaluvlnv")
def form_legit_data_ask(callback):
    msg = 'От вас для проверки требуется:\n\nЕсли вы покупатель:\nСсылку на продавца или объявление\nФотографии проверяемого айтема а также каждой бирки отдельно с хорошим освещением\n\nЕсли вы продавец:\nСсылку на продавца или сайт откуда покупалась вещь\nФотографии проверяемого айтема а также каждой бирки отдельно с хорошим освещением\n\nПосле ввода данных напишите end или /end'
    bot.send_message(callback.message.chat.id, msg)
    legiter_name = callback.message.json['reply_markup']['inline_keyboard'][0][0]['text']
    bot.register_next_step_handler(callback.message, form_legit_data_collect, legiter_name)


@bot.callback_query_handler(func=lambda call: call.data == "form_legit_data_collect_roysmort")
def form_legit_data_ask(callback):
    msg = 'От вас для проверки требуется:\n\nЕсли вы покупатель:\nСсылку на продавца или объявление\nФотографии проверяемого айтема а также каждой бирки отдельно с хорошим освещением\n\nЕсли вы продавец:\nСсылку на продавца или сайт откуда покупалась вещь\nФотографии проверяемого айтема а также каждой бирки отдельно с хорошим освещением\n\nПосле ввода данных напишите end или /end'
    bot.send_message(callback.message.chat.id, msg)
    legiter_name = callback.message.json['reply_markup']['inline_keyboard'][1][0]['text']
    print(callback.message.json['reply_markup']['inline_keyboard'][1][0])
    bot.register_next_step_handler(callback.message, form_legit_data_collect, legiter_name)


def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


@bot.message_handler(content_types=['photo'])
def save_photo(message):
    Path(f'files/{message.chat.id}/photos').mkdir(parents=True, exist_ok=True)
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    print(file_info.file_path)
    src = f'files/{message.chat.id}/' + file_info.file_path
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    with open(f'files/{message.chat.id}/{file_info.file_path}', "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    try:
        conn = sqlite3.connect('orders.db')
        cur = conn.cursor()
        sql_select_query = """INSERT INTO legit_orders (userid, chatid, time_sent, photo) VALUES (?, ?, ?, ?)"""
        name = message.from_user.first_name
        username = message.from_user.username
        time_message_sent = datetime.now()
        data_tuple = (username, name, time_message_sent, encoded_string)
        cur.execute(sql_select_query, data_tuple)
        conn.commit()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


def save_photo_single(message):
    Path(f'files/{message.chat.id}/photos').mkdir(parents=True, exist_ok=True)
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    print(file_info.file_path)
    src = f'files/{message.chat.id}/' + file_info.file_path
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    with open(f'files/{message.chat.id}/{file_info.file_path}', "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    return encoded_string


def show_photo(ID, img):
    with open("files/imageToSave.jpg", "wb") as fh:
        fh.write(base64.decodebytes(img))
        bot.send_photo(ID, open("files/imageToSave.jpg", "rb"))



def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


def form_legit_data_collect(message, legiter_name):
    if message.content_type == 'photo':
        encoded_str = save_photo(message)
        try:
            conn = sqlite3.connect('orders.db')
            cur = conn.cursor()
            sql_select_query = """INSERT INTO legit_orders (userid, chatid, time_sent, photo) VALUES (?, ?, ?, ?)"""
            name = message.from_user.first_name
            username = message.from_user.username
            time_message_sent = datetime.now()
            data_tuple = (username, name, time_message_sent, encoded_str)
            cur.execute(sql_select_query, data_tuple)
            conn.commit()
            bot.register_next_step_handler(message, form_legit_data_collect, legiter_name)
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

    if message.content_type == 'text' and message.text != '/end' and message.text != 'end':
        try:
            conn = sqlite3.connect('orders.db')
            cur = conn.cursor()
            sql_select_query = """INSERT INTO legit_orders (userid, chatid, time_sent, link) VALUES (?, ?, ?, ?)"""
            name = message.from_user.first_name
            username = message.from_user.username
            time_message_sent = datetime.now()
            data_tuple = (username, name, time_message_sent, message.text)
            cur.execute(sql_select_query, data_tuple)
            conn.commit()
            bot.register_next_step_handler(message, form_legit_data_collect, legiter_name)
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

    elif message.text == '/end' or message.text == 'end':
        legit_app(legiter_name, message)


@bot.callback_query_handler(func=lambda call: call.data == "cancel_order")
def cancel_order(call):
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    start_message(call.message)


@bot.callback_query_handler(func=lambda call: call.data == "frm1")
def form1(callback):
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Отменить', callback_data="cancel_order")
    kb.row(btn1)
    bot.send_message(callback.message.chat.id, 'Отправьте ссылку на товар', reply_markup=kb)
    bot.register_next_step_handler(callback.message, form2)


def form2(message):
    text = message.text
    bot.send_message(message.chat.id, 'Отправьте размер товара')
    bot.register_next_step_handler(message, form3, text)


def form3(message, text):
    text1 = message.text

    bot.send_message(message.chat.id, 'Отправьте цену товара в ¥ (юань)')
    bot.register_next_step_handler(message, form4, text, text1)


def form4(message, text, text1):
    text2 = message.text
    msg = 'Отправьте фотографию где видны размер и цвет товара, чтобы мы не ошиблись с заказом'

    bot.send_photo(message.chat.id, 'https://i.imgur.com/7uovKLu.jpg', caption=msg)
    bot.register_next_step_handler(message, form5, text, text1, text2)


def form5(message, text, text1, text2):
    if message.content_type == 'photo':
        text3 = save_photo_single(message)
        msg = 'Введите номер телефона, чтобы бы могли с Вами связаться'

        bot.send_message(message.chat.id, msg)
        bot.register_next_step_handler(message, form6, text, text1, text2, text3)
    else:
        bot.send_message(message.chat.id, 'Повторите попытку, вы отправили НЕ фотографию.')
        form4(message, text, text1)



def form6(message, text, text1, text2, text3):
    text4 = message.text
    msg = 'ФИО\nВведите Вашу фамилию, имя и отчество(если имеется)'

    bot.send_message(message.chat.id, msg)
    bot.register_next_step_handler(message, form_order, text, text1, text2, text3, text4)


def form_order(message, text, text1, text2, text3, text4):
    text5 = message.text

    msg = 'Напишите тип выдачи заказа(СДЭК или самовывоз(г. Москва))'

    bot.send_message(message.chat.id, msg)
    bot.register_next_step_handler(message, form7, text, text1, text2, text3, text4, text5)


def form7(message, text, text1, text2, text3 ,text4, text5):
    kurs =


    if message.text == 'сдэк' or message.text == 'СДЭК':
        bot.send_message(message.chat.id, '''
Введите данные для отправки товара:
город и ближайшее к Вам отделение СДЭК
''')
        data_t = data_temp()
        name = message.from_user.first_name
        username = message.from_user.username
        time_message_sent = datetime.now()
        data_t.user = [username, time_message_sent, text, text1, text2, text3, text4, text5, message.text]
        bot.register_next_step_handler(message, get_adress, data_t.user)


    elif message.text == 'самовывоз' or message.text == 'САМОВЫВОЗ':
        data_t = data_temp()
        name = message.from_user.first_name
        username = message.from_user.username
        time_message_sent = datetime.now()
        data_t.user = [username, time_message_sent, text, text1, text2, text3, text4, text5]
        try:
            # print(data_t.user)
            data_t.user.append(message.text)
            user = tuple(data_t.user)
            data_t.cart.append(user)
            # print(user)
            conn = sqlite3.connect('orders.db')
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO orders(userid, time_sent, model, size, price, photo_check, F_I_O, phone_number, order_type) VALUES(?,?,?,?,?,?,?,?,?);",
                user)
            conn.commit()
            msg = f"""
_______________________

Итоговая цена составит{price} руб.
Курс юаня к рублю {kurs}
_______________________

В заказе товары: 
- {text}, Размер : {text1} на {text2} юаней, №

Курс юаня к рублю {'14.6'}

Самовывоз происходит по адреса: Ул. Башиловская д.17
Номер телефона:{text4}
ФИО: {text5}

Если вы хотите изменить данные, нажмите на кнопку Изменить адрес

Выкуп товара происходит в течение 24 часов после оплаты. 
Если при выкупе цена изменится, мы свяжемся с вами для доплаты|возврата средств.

_______________________

Если Вас устраивает, переведите {'1488'} руб. на следующую карту Tinkoff
5536913951705017 Линьков. В
_____________________

Осуществляя перевод, вы подтверждаете что корректно указали товар, его характеристики и согласны со сроками доставки. 
Мы не несем ответственности за соответствие размеров и брак.

Оплатите и нажмите кнопку Подтвердить оплату✅"""

            bot.send_message(message.chat.id, msg)
            admin_app(ADMIN_ID, tuple(data_t.user))

        except:
            print('Exception form3')


def get_adress(message, user):
    print(message.text)
    print(user)
    user.append(message.text)
    # data_t.user = [username, time_message_sent, text, text1, text2, text3, text4, text5, message.text]
    msg = f"""
_______________________

Итоговая цена составит {'1488'} руб.
Курс юаня к рублю {'14.6'}

_______________________

В заказе товары: 
- {user[2]}, Размер : {user[3]} на {user[4]} юаней, №

Курс юаня к рублю {'14.6'}

Доставка ИЗ Москвы оплачивается отдельно напрямую СДЭКу
Отправим ваш заказ по адресу:
{message.text}
{user[6]}

ФИО: {user[7]}

Если вы хотите изменить данные, нажмите на кнопку Изменить адрес✏️

Выкуп товара происходит в течение 24 часов после оплаты. 
Если при выкупе цена изменится, мы свяжемся с вами для доплаты|возврата средств.

_______________________

Если Вас устраивает, переведите {'1488'} руб. на следующую карту Tinkoff
5536913951705017 Линьков. В

_______________________ч

Осуществляя перевод, вы подтверждаете что корректно указали товар, его характеристики и согласны со сроками доставки. 
Мы не несем ответственности за соответствие размеров и брак.
Оплатите и нажмите кнопку Подтвердить оплату✅"""

    print(len(msg))
    user = tuple(user)
    # data_t.cart.append(user)
    # print(user)
    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()
    print(len(user))
    cur.execute("INSERT INTO orders(userid, time_sent, model, size, price, photo_check, F_I_O, phone_number, order_type, adress) VALUES(?,?,?,?,?,?,?,?,?,?);",
        user)
    conn.commit()
    bot.send_message(message.chat.id, msg)
    admin_app(ADMIN_ID, tuple(user))


def admin_app(ADMIN_ID, user):
    if len(user) == 10:
        print(user)
        ankets = f'''Новый заказ от @{user[0]}!
        Время: {user[1]}
        Ссылка на пару: {user[2]}
        Размер пары: {user[3]}
        Цена пары в ¥: {user[4]}
        Скриншот:
        Номер телефона: {user[6]}
        ФИО: {user[7]}
        Тип выдачи заказа:{user[8]}
        Адрес: {user[9]}
        '''
        with open("files/imageToSave.jpg", "wb") as fh:
            fh.write(base64.decodebytes(user[5]))
            bot.send_photo(ADMIN_ID, open("files/imageToSave.jpg", "rb"), caption=ankets)

        data_temp.clear(data_temp)

    elif len(user) == 9:
        print(user)
        ankets = f'''Новый заказ от @{user[0]}!
                Время: {user[1]}
                Ссылка на пару: {user[2]}
                Размер пары: {user[3]}
                Цена пары в ¥: {user[4]}
                Скриншот:
                Номер телефона: {user[6]}
                ФИО: {user[7]}
                Тип выдачи заказа: {user[8]}
                '''
        with open("files/imageToSave.jpg", "wb") as fh:
            fh.write(base64.decodebytes(user[5]))
            bot.send_photo(ADMIN_ID, open("files/imageToSave.jpg", "rb"), caption=ankets)

        data_temp.clear(data_temp)

    else:
        print(len(user))
        print('ERROR')


def legit_app(legiter_name, message):
    bot.send_message(message.chat.id, 'ABOBA')
    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()
    sql_select_query = """SELECT chatid from legiters where userid = ?"""
    cur.execute(sql_select_query, (legiter_name, ))
    legiter_id = cur.fetchall()
    bot.send_message(legiter_id[0][0], f'Вам пришла заявка от @{message.from_user.username} на легит:\n')

    sql_select_query = """SELECT photo, link, time_sent from legit_orders where userid = ?"""
    cur.execute(sql_select_query, (message.from_user.username, ))
    customer_id = cur.fetchall()

    for i in range(len(customer_id)):
        # print(customer_id[i][0])
        if customer_id[i][0] is None:
            i += 1

        else:
            show_photo(legiter_id, customer_id[i][0])


if __name__ == '__main__':
    init_table()
    bot.polling(none_stop=True)



