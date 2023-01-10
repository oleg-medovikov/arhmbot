from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from clas import User, Person, EventHistory

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

    USER = await User.get(query.message['chat']['id'])
    PERSON = await Person.get(USER.u_id)

    kb_game = InlineKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
        )

    # если не закончено событие, предложить его закончить
    if await EventHistory.get(PERSON.p_id) is not None:
        kb_game.add(InlineKeyboardButton(
             text='понимаю',
             callback_data='get_event'
             ))
        return await query.message.answer(
                 'У вас незаконченное событие!',
                 reply_markup=kb_game,
                 parse_mode='Markdown'
                 )
    # вытаскиваем статус персонажа, чтобы проверить его состояние
    MESS = ''
    # если персонаж умер, вовращаем сообщение о смерти
    if DIE:
        return await query.message.answer(MESS, parse_mode='Markdown')

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
