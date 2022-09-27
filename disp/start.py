from .dispetcher import dp, bot
from aiogram.utils.callback_data import CallbackData
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text

from func import cheak_user, cheak_person, login_user, person_status

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
    
   # удалим команду start  для чистоты
    try:
        await message.delete()
    except:
        pass
    MESS = 'Вы попали в адаптацию настольной игры "Ужас Аркхэма". Помните, что в этом городе чужаков не любят, и если и не пошлют, то нагрубить могут вполне. Вы согласны стойко вытерпеть пренебрежительное отношение горожан? (+16)'
    kb_agreement = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
            .add(InlineKeyboardButton(text='Согласиться',  callback_data='start_new_game'))
    
    await message.answer(MESS, reply_markup= kb_agreement ) 

@dp.callback_query_handler(Text(equals=['start_new_game']))
async def start_new_game(query: types.CallbackQuery):
    await query.message.edit_reply_markup(reply_markup=None)
    bot_user = query.message['chat']['id']
    # проверяем зарегистрирован ли пользователь
    if not cheak_user(bot_user):
        # если не зарегистрирован
        HELLO_MESS = get_hello_start() + 'искатель приключений!'\
            + '\nДо тебя дошли слухи, что в городе Аркхеме творится нечто загадочное? Глупые сказки пьяных рыбаков будоражут фантазию настолько, что это стоит потраченного времени? Ты очень странный человек, раз решил провести свой отпуск в этом задрипанном городишке. Твои планы туманны, а действия вызывают подозрения. А мы не любим подозрительных личностей. Мы будем следить за тобой. А то вдруг, ты отважишься бросить вызов Древнему Ужасу?'

        await query.message.answer( HELLO_MESS ) 
        kb_hello = InlineKeyboardMarkup( resize_keyboard=True, one_time_keyboard=True)\
            .add(InlineKeyboardButton(text='Пройти анкету',    callback_data='register'))\
            .add(InlineKeyboardButton(text='Прочесть правила', callback_data='rules'))
 
        MESS = 'Так как вы впервые прибыли в наш город, заполните небольшую анкету о себе. Желательно, ознакомьтесь с правилами поведения в городе. Это повысит ваши шансы.'
        return await query.message.answer(MESS, reply_markup=kb_hello)
    else:
        login_user(bot_user)
    
    # проверяем наличие живого персонажа
    if not cheak_person(bot_user):
        # если нет живого персонажа, нужно его завести
        HELLO_MESS = get_hello_start() + 'искатель приключений!'\
                + '\nПри взгляде на Вас я испытываю лёгкое чувство дежавю. Возможно, Вы уже посещали наш прекрасный город Аркхэм? Тем не менее, вам стоит зарегистрироваться ещё раз.'
        
        await query.message.answer( HELLO_MESS ) 
        kb_hello = InlineKeyboardMarkup( resize_keyboard=True, one_time_keyboard=True)\
            .add(InlineKeyboardButton(text='Пройти анкету',    callback_data='register'))\
            .add(InlineKeyboardButton(text='Прочесть правила', callback_data='rules'))
            
        MESS = 'Чистый бланк лежит перед вами. Так же не забывайте о возможности ознакомиться с правилами поведения в городе. Это повысит ваши шансы.'
        return await query.message.answer(MESS, reply_markup=kb_hello)
    else:
        # если персонаж жив, показываем его статус
        return await query.message.answer(person_status( bot_user ) , parse_mode='Markdown')
