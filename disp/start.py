from .dispetcher import dp, bot
from aiogram.utils.callback_data import CallbackData
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from func import cheak_user

import time

def get_hello_start():
    temp = int(time.strftime("%H"))
    return {
         0   <= temp   < 6  :  'Доброй ночи, ',
         6   <= temp   < 11 :  'Доброе утро, ',
         11  <= temp   < 16 :  'Добрый день, ',
         16  <= temp   < 22 :  'Добрый вечер, ',
         22  <= temp   < 24 :  'Доброй ночи, '
    }[True]

@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    bot_user = message['from']['id']
    
    HELLO_MESS = get_hello_start() + 'искатель приключений!'\
            + '\nДо тебя дошли слухи, что в городе Аркхеме творится нечто загадочное? Глупые сказки пьяных рыбаков будоражут фантазию настолько, что это стоит потраченного времени? Ты очень странный человек, раз решил провести свой отпуск в этом задрипанном городишке. Твои планы туманны, а действия вызывают подозрения. А мы не любим подозрительных личностей. Мы будем следить за тобой. А то вдруг, ты отважишься бросить вызов Древнему Ужасу?'

    await message.answer( HELLO_MESS ) 
    # удалим команду start  для чистоты
    try:
        await message.delete()
    except:
        pass

    # проверяем зарегистрирован ли пользователь 
    if not cheak_user(bot_user):
        # если не зарегистрирован
        kb_hello = InlineKeyboardMarkup( resize_keyboard=True, one_time_keyboard=True)\
            .add(InlineKeyboardButton(text='Пройти анкету',    callback_data='register'))\
            .add(InlineKeyboardButton(text='Прочесть правила', callback_data='rules'))
 
        MESS = 'Так как вы впервые прибыли в наш город, заполните небольшую анкету о себе. Желательно, ознакомьтесь с правилами поведения в городе. Это повысит ваши шансы.'
        await message.answer(MESS, reply_markup=kb_hello)

