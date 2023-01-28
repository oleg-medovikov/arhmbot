from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from clas import PersonStatus, Inventory

from func import inventory_mess, update_message
from conf import emoji

equip_slots = [
    'head', 'onehand', 'twohands',
    'head', 'body', 'legs', 'shoes'
    ]


@dp.callback_query_handler(Text(equals=['inventory_equip_items']))
async def inventory_equip_items(query: types.CallbackQuery):
    "показываем игроку список надетых вещей"
    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])

    INV = await Inventory.get(PERS.p_id)

    MESS = inventory_mess(PERS, INV, EQUIP=True)

    kb_bag = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )

    for item in INV:
        if item['slot'] in equip_slots:
            kb_bag.add(InlineKeyboardButton(
                text=emoji(item['emoji']) + ' ' + item['name'],
                callback_data='inventory_equip_item_' + str(item['i_id'])
                    ))

    kb_bag.add(InlineKeyboardButton(
        text='назад',
        callback_data='inventory_main',
        ))
    return await update_message(
            query.message,
            MESS,
            kb_bag)
