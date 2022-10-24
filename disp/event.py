from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton, message

import json 
from func import make_get_event, make_finish_event

@dp.callback_query_handler(Text(equals=['get_event']))
async def person_get_event(query: types.CallbackQuery):
    # удаляем предыдущую клавиатуру
    await query.message.edit_reply_markup( reply_markup=None )
    U_ID = query.message['chat']['id']
    EVENT =  make_get_event( U_ID )
    
    kb_event = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    if 'error' in EVENT.keys():
        kb_event.add(InlineKeyboardButton(
            text = 'Понимаю', callback_data='continue_game'
            ))
        return await query.message.answer(EVENT['MESS'], reply_markup=kb_event, parse_mode='Markdown' )

    MESS = EVENT['description']
    MESS = f'``` {MESS} ```'

    if EVENT['choice']:
        BUTTONS = json.loads( EVENT['check'])['choice']
        
        kb_event.add(InlineKeyboardButton(
                text = BUTTONS[0], callback_data='event_' + str(EVENT['e_id']) + '_1'
                ))
        kb_event.add(InlineKeyboardButton(
                text = BUTTONS[1], callback_data='event_' + str(EVENT['e_id']) + '_0'
                ))
    else:
        kb_event.add(InlineKeyboardButton(
                text = 'Понимаю', callback_data='event_' + str(EVENT['e_id']) + '_0' 
                ))
 
    return await query.message.answer(MESS, reply_markup=kb_event, parse_mode='Markdown' )


@dp.callback_query_handler(Text(startswith=['event_']))
async def person_finish_event(query: types.CallbackQuery):
    # удаляем предыдущую клавиатуру
    await query.message.edit_reply_markup( reply_markup=None )
    U_ID = query.message['chat']['id']
    CHOICE = int(query['data'].split('_')[-1])

    ERROR, MESS = make_finish_event( U_ID, CHOICE )

    kb_event = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
            .add(InlineKeyboardButton(text = 'Понимаю', callback_data='continue_game') ) 

    return await query.message.answer( MESS, reply_markup=kb_event, parse_mode='Markdown' )




 
