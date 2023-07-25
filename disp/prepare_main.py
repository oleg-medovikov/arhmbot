from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from clas import PersonStatus, String
from func import update_message


@dp.callback_query_handler(Text(equals=['prepare_main']))
async def prepare_main(query: types.CallbackQuery):
    """
    тут персонаж будет подготавливаться к ходу
    возможные действия:
    1) почитать историю персонажа
    2) почитать дневник событий
    3) зайти в инвентарь
    4) посмотреть друзей
    5) посмотреть достижения персонажа
    """

    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])
    MESS = await String.get(f'person_prepare_{PERS.profession}')
    kb_prepare = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )
    DICT = {
        'основная цель':       'prepare_main_quest',
        'история перемещений': 'prepare_relocations_0',
        'инвентарь':           'inventory_main',
        'назад':               'continue_game',
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
