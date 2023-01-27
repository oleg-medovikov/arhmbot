from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from clas import PersonStatus, Item, Inventory, DropItem, String
from func import update_message


@dp.callback_query_handler(Text(startswith=['inventory_drop_item_ask_']))
async def inventory_drop_item_ask(query: types.CallbackQuery):
    "перед тем как выбросить предмет, спрашиваем, что оставить в записке"

    I_ID = query.data.split('_')[-1]

    MESS = await String.get('drop_items_ask')

    kb_bag = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )

    DICT = {
        'подарить предмет нашедшему':   f'drop_ask_good_{I_ID}',
        'попросить не трогать предмет': f'drop_ask_bad_{I_ID}',
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


@dp.callback_query_handler(Text(startswith=[
                                    'drop_ask_good_',
                                    'drop_ask_bad_'
                                    ]))
async def inventory_drop_item(query: types.CallbackQuery):
    "Выбрасываем предмет из сумки и оставляем его на локации"

    I_ID = int(query.data.split('_')[-1])
    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])

    S_NAME = {
        'good' in query.data: f'drop_item_good_{PERS.profession}',
        'bad' in query.data:  f'drop_item_bad_{PERS.profession}',
            }[True]
    NOTE = await String.get(S_NAME)

    ITEM = await Item.get(I_ID)

    DROPITEM = DropItem(**{
        'node_id':   STAT.location,
        'i_id':      I_ID,
        'stage':     STAT.stage,
        'gamename':  PERS.gamename,
        'comment':   NOTE,
        })
    await DROPITEM.new()

    await Inventory.drop(PERS.p_id, I_ID)

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
            ITEM.drop_mess,
            kb_bag
            )
