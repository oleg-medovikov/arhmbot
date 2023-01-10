from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from func import get_game_status, get_look_around,\
        get_locations_nearby, make_relocation

"""
    1. показать игроку частичный статус
    2. предложить осмотреться
    3. предложить меню со статусом и инвентарем
    3. предложить меню с перемещением куда двигаться
"""


@dp.callback_query_handler(Text(equals=['continue_game']))
async def continue_game(query: types.CallbackQuery):
    "Непосредственно игра!"
    # удаляем предыдущую клавиатуру
    await query.message.edit_reply_markup(reply_markup=None)

    U_ID = query.message['chat']['id']
    MESS, DIE, EVENT = get_game_status(U_ID)

    # если персонаж умер, вовращаем сообщение о смерти
    if DIE:
        return await query.message.answer(MESS, parse_mode='Markdown')

    kb_game = InlineKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
        )

    # если не закончено событие, предложить его закончить
    if EVENT:
        kb_game.add(InlineKeyboardButton(
             text='понимаю',
             callback_data='get_event'
             ))
        return await query.message.answer(
                 MESS,
                 reply_markup=kb_game,
                 parse_mode='Markdown'
                 )

    # если с персонажем все нормально, предложить что-то сделать
    DICT = {
        'осмотреться':       'look_around',
        'статус персонажа':  'status',
        'действовать':       'get_event',
        'уйти куда-то ещё':  'leave',
        }

    for key, value in DICT.items():
        kb_game.add(InlineKeyboardButton(
            text=value,
            callback_data=key
            ))
    return await query.message.answer(
            MESS,
            reply_markup=kb_game,
            parse_mode='Markdown'
            )
