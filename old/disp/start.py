from conf.message import MESS_anketa_second, MESS_hello_login
from .dispetcher import dp
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text

from func import check_user, check_person, person_status
from conf import MESS_disclaimer, MESS_hello_nologin, MESS_anketa_first,\
                 MESS_hello_login, MESS_anketa_second

@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
   # только показываем дисклеймер и просим согласиться с жестокостью 
   # удалим команду start  для чистоты
    try:
        await message.delete()
    except: pass
    kb_agreement = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
            .add(InlineKeyboardButton(text='Согласиться',  callback_data='start_new_game'))
    await message.answer(MESS_disclaimer, reply_markup= kb_agreement ) 

@dp.callback_query_handler(Text(equals=['start_new_game']))
async def start_new_game(query: types.CallbackQuery):
    await query.message.edit_reply_markup(reply_markup=None)
    bot_user = query.message['chat']['id']
    # проверяем зарегистрирован ли пользователь
    if not check_user(bot_user):
        # если не зарегистрирован
        await query.message.answer( MESS_hello_nologin ) 
        kb_hello = InlineKeyboardMarkup( resize_keyboard=True, one_time_keyboard=True)\
            .add(InlineKeyboardButton(text='Пройти анкету',    callback_data='register'))\
            .add(InlineKeyboardButton(text='Прочесть правила', callback_data='manual'))
        # просим пройти анкету, переходим на регистрацию
        return await query.message.answer( MESS_anketa_first, reply_markup=kb_hello)
    
    # если зарегистрированный пользователь, то проверяем наличие живого персонажа
    if not check_person(bot_user):
        # если нет живого персонажа, нужно его завести
       
        await query.message.answer( MESS_hello_login ) 
        kb_hello = InlineKeyboardMarkup( resize_keyboard=True, one_time_keyboard=True)\
            .add(InlineKeyboardButton(text='Пройти анкету',    callback_data='register'))\
            .add(InlineKeyboardButton(text='Прочесть правила', callback_data='manual'))
            
        return await query.message.answer(MESS_anketa_second, reply_markup=kb_hello)
    else:
        # если персонаж жив, показываем его статус
        kb_game = InlineKeyboardMarkup( resize_keyboard=True, one_time_keyboard=True)\
                .add(InlineKeyboardButton(text='Продолжить игру',  callback_data='continue_game'))\
                .add(InlineKeyboardButton(text='Прочесть правила', callback_data='manual'))
        return await query.message.answer(person_status( bot_user ) , parse_mode='Markdown', reply_markup=kb_game )
