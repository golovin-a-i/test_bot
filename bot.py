from email import message
import telebot
from telebot import types
import pandas as pd
import random

bot = telebot.TeleBot('5540462908:AAGmh0-xWLtPdvYwFOjyy1CyDfMk_s4_LUU')

chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
length_id_user = 8



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет!\n")
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton('Регистрация')
    item_2 = types.KeyboardButton('Цены')
    markup.add(item, item_2)
    # markup.add(item_2)
    bot.send_message(message.chat.id, "Выберите одну из кнопок.", reply_markup=markup)

@bot.message_handler(commands=['reg'])
def start(message):
    bot.send_message(message.from_user.id, "Как тебя зовут?")
    bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name

name = ''
surname = ''
age = 0


def get_name(message): #получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    global age
    while age == 0:
        try:
                age = int(message.text) #проверяем, что возраст введен корректно
        except Exception:
                bot.send_message(message.from_user.id, 'Цифрами, пожалуйста, введите еще раз')
                age = 0
                bot.register_next_step_handler(message, get_age)
    keyboard = types.InlineKeyboardMarkup() #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes') #кнопка «Да»
    keyboard.add(key_yes) #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = f'Тебе {str(age)} лет, тебя зовут {name} {surname}?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global age
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        
        df = pd.read_csv("test_data.csv", index_col=0)
        id_user = ''
        for i in range(length_id_user):
            id_user += random.choice(chars)
        df = df.append({'id': id_user, 'name': name, 'surname': surname, 'age': age}, ignore_index=True)
        df.to_csv('test_data.csv')
        age = 0
        bot.send_message(call.message.chat.id, 'Запомню :)')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Не запомню :)')
        age = 0

@bot.message_handler(content_types=['text'])
def some_message(message):
    if message.text == 'some':
        bot.send_message(message.from_user.id, 'Нажми /start или /reg')
    elif message.text == 'Регистрация':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        # item1=types.KeyboardButton("Кнопка 2")
        # markup.add(item1)
        bot.send_message(message.chat.id,'Выберите что вам надо', reply_markup=markup)
        start(message)




bot.infinity_polling()
        

