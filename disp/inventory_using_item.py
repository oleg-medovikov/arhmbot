from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text

from clas import PersonStatus
from func import update_message, using_item, create_keyboard


@dp.callback_query_handler(Text(startswith=['inventory_using_item_']))
async def inventory_using_item(query: types.CallbackQuery):
    "Используем предмет"

    I_ID = int(query.data.split('_')[-1])

    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])

    MESS = await using_item(PERS, STAT, I_ID)

    DICT = {
        'назад': 'inventory_main',
        }

    return await update_message(
            query.message,
            MESS,
            create_keyboard(DICT)
            )
