from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from clas import Manual, String
from conf import emoji_all, emoji
from func import update_message


@dp.callback_query_handler(Text(equals=['manual']))
async def kb_full_manual(query: types.CallbackQuery):
    "тут нужно предложить весь список ссылок на мануал"

    kb_man = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for man in await Manual.get_all_manual():
        kb_man.add(InlineKeyboardButton(
            text=man.m_name,
            callback_data=f'manual_{man.m_id}',
            ))

    kb_man.add(InlineKeyboardButton(
        text='Прекратить читать правила',
        callback_data='start_new_game'
        ))

    return await update_message(
        query.message,
        await String.get('manual_hello'),
        kb_man
        )


@dp.callback_query_handler(Text(startswith=['manual_']))
async def answer_man_buttom(query: types.CallbackQuery):

    M_ID = int(query.data.split('_')[-1])
    MESS = await Manual.get(M_ID)

    for key in emoji_all():
        if key in MESS:
            MESS = MESS.replace(key, emoji(key))

    kb_man = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb_man.add(InlineKeyboardButton(
        text='назад',
        callback_data='manual'
        ))
    return await update_message(query.message, MESS, kb_man)
