from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text

from clas import PersonStatus, String
from func import update_message, create_keyboard


@dp.callback_query_handler(Text(equals=['prepare_main_quest']))
async def prepare_main_quest(query: types.CallbackQuery):
    """показать игроку основной квест"""

    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])
    MESS = await String.get(f'main_quest_{STAT.stage}_{PERS.profession}')
    DICT = {
        'назад': 'prepare_main',
    }

    return await update_message(
            query.message,
            MESS,
            create_keyboard(DICT)
    )
