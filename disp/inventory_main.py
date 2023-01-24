from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from clas import PersonStatus, Inventory

from func import inventory_mess, update_message
from conf import emoji


@dp.callback_query_handler(Text(equals=['inventory_main']))
async def inventory_main(query: types.CallbackQuery):
    "показываем игроку инвентарь персонажа"
    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])

    INV = await Inventory.get(PERS.p_id)

    MESS = inventory_mess(PERS, INV)

    kb_bag = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )

    for item in INV:
        if item['slot'] in ('bag'):
            kb_bag.add(InlineKeyboardButton(
                text=emoji(item['emoji']) + ' ' + item['name'],
                callback_data='inventory_bag_item_' + str(item['i_id'])
                    ))

    kb_bag.add(InlineKeyboardButton(
        text='Экипированные вещи',
        callback_data='inventory_equip_items',
        ))

    kb_bag.add(InlineKeyboardButton(
        text='назад',
        callback_data='continue_game',
        ))
    return await update_message(
            query.message,
            MESS,
            kb_bag)
