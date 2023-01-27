from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from clas import PersonStatus, Item, Inventory, DropItem
from func import update_message


@dp.callback_query_handler(Text(startswith=['inventory_drop_item_']))
async def inventory_drop_item(query: types.CallbackQuery):
    "Выбрасываем предмет из сумки и оставляем его на локации"

    I_ID = int(query.data.split('_')[-1])

    ITEM = await Item.get(I_ID)

    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])

    MESS = ITEM.drop_mess

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
