from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from func import get_manual, get_manual_text
from conf import emoji

@dp.callback_query_handler(Text(equals=['manual']))
async def kb_full_manual(query: types.CallbackQuery):
    "тут нужно предложить весь список ссылок на мануал"
    "удаляем предыдущую клаву"
 
    await query.message.edit_reply_markup( reply_markup=None )

    MANUAL = get_manual( query.message['chat']['id'] )

    kb_man = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for row in MANUAL:
        kb_man.add(InlineKeyboardButton(
            text=row.get('m_name'),
            callback_data='manual_' + str(row.get('m_id')) ))

    kb_man.add(InlineKeyboardButton(
        text='Прекратить читать правила',
        callback_data='start_new_game'
        ))

    MESS = 'Правила поведения в Архэме представляют собой несколько буклетов, какой из них хотите прочитать?'

    await query.message.answer(MESS, reply_markup= kb_man )


@dp.callback_query_handler(Text(startswith=['manual_'] ))
async def answer_man_buttom(query: types.CallbackQuery):
    
    M_ID = int(query.data.split('_')[-1]) 
    U_ID = query.message['chat']['id']
    MESS = get_manual_text ( U_ID, M_ID)

    for key, value in emoji.items():
        if key in MESS:
            MESS = MESS.replace( key, value )

    await query.message.answer( MESS )
