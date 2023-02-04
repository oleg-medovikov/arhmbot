from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from clas import PersonStatus, Shop, Item
from func import update_message, demand
from conf import emoji


@dp.callback_query_handler(Text(startswith=['go_to_the_shop']))
async def go_to_the_shop(query: types.CallbackQuery):
    "Заходим в магазин"

    S_ID = int(query.data.split('_')[-1])

    SHOP = await Shop.get_by_id(S_ID)
    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])

    kb_shop = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )

    DICT = dict()

    if demand(PERS, STAT, SHOP.get_demand()):
        # если персонаж проходит требования магазина
        MESS = SHOP.mess_welcome
        for ITEM in await Item.get_by_list(SHOP.product_list):
            DICT[emoji(ITEM.emoji) + ' ' + ITEM.name] = f'buy_item_{ITEM.i_id}'
        DICT['уйти'] = 'continue_game'
    else:
        # если не проходит требования
        MESS = SHOP.mess_not_pass
        DICT['понятно'] = 'continue_game'

    for key, value in DICT.items():
        kb_shop.add(InlineKeyboardButton(
            text=key,
            callback_data=value
                ))

    return await update_message(
            query.message,
            MESS,
            kb_shop
            )
