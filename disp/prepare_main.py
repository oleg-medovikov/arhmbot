from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text

from clas import PersonStatus, String
from func import update_message, create_keyboard


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
    DICT = {
        'основная цель':        'prepare_main_quest',
        'история перемещений':  'prepare_relocations_0',
        'карта':               f'prepare_map_{STAT.p_id}',
        'инвентарь':            'inventory_main',
        'назад':                'continue_game',
    }

    return await update_message(
            query.message,
            MESS,
            create_keyboard(DICT)
    )
