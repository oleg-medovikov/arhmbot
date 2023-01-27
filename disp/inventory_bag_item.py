from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from clas import Item
from func import update_message


@dp.callback_query_handler(Text(startswith=['inventory_bag_item']))
async def inventory_bag_item(query: types.CallbackQuery):
    "показываем игроку описание предмета и действия с ним"

    I_ID = int(query.data.split('_')[-1])
    ITEM = await Item.get(I_ID)

    kb_bag = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )

    DICT = {
        'Использовать предмет': f'inventory_using_item_{I_ID}',
        'Выбросить предмет':    f'inventory_drop_item_ask_{I_ID}',
        'назад':                'inventory_main',
        }

    for key, value in DICT.items():
        kb_bag.add(InlineKeyboardButton(
            text=key,
            callback_data=value,
            ))

    return await update_message(
            query.message,
            ITEM.description,
            kb_bag)
