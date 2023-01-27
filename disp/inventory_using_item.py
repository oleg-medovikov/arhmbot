from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from clas import PersonStatus
from func import update_message, using_item


@dp.callback_query_handler(Text(startswith=['inventory_using_item_']))
async def inventory_using_item(query: types.CallbackQuery):
    "Используем предмет"

    I_ID = int(query.data.split('_')[-1])

    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])

    MESS = await using_item(PERS, STAT, I_ID)

    kb_bag = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )

    DICT = {
        'назад': 'inventory_main',
        }

    for key, value in DICT.items():
        kb_bag.add(InlineKeyboardButton(
            text=key,
            callback_data=value,
            ))

    return await update_message(
            query.message,
            MESS,
            kb_bag
            )
