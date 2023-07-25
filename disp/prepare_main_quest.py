from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from clas import PersonStatus, String
from func import update_message


@dp.callback_query_handler(Text(equals=['prepare_main_quest']))
async def prepare_main_quest(query: types.CallbackQuery):
    """показать игроку основной квест"""

    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])
    MESS = await String.get(f'main_quest_{STAT.stage}_{PERS.profession}')
    kb_prepare = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )
    DICT = {
        'назад': 'prepare_main',
    }

    for KEY, VALUE in DICT.items():
        kb_prepare.add(InlineKeyboardButton(
            text=KEY,
            callback_data=VALUE,
        ))

    return await update_message(
            query.message,
            MESS,
            kb_prepare)
