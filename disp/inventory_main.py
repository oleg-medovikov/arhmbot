from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from clas import User, Person, Inventory

from func import inventory_mess
from conf import emoji


@dp.callback_query_handler(Text(equals=['inventory_main']))
async def inventory_main(query: types.CallbackQuery):
    "показываем игроку инвентарь персонажа"
    # удаляем предыдущую клавиатуру
    await query.message.edit_reply_markup(reply_markup=None)
    U_ID = query.message['chat']['id']

    USER = await User.get(U_ID)
    PERSON = await Person.get(USER.u_id)

    INV = await Inventory.get(PERSON.p_id)

    MESS = inventory_mess(PERSON, INV)

    kb_bag = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )

    for item in INV:
        if item['slot'] in ('bag'):
            kb_bag.add(InlineKeyboardButton(
                text=emoji(item['emoji']) + ' ' + item['name'],
                callback_data='bag_item_' + str(item['i_id'])
                    ))

    kb_bag.add(InlineKeyboardButton(
        text='Экипированные вещи',
        callback_data='inventory_equip_items',
        ))

    kb_bag.add(InlineKeyboardButton(
        text='назад',
        callback_data='continue_game',
        ))

    return await query.message.answer(
            MESS,
            reply_markup=kb_bag,
            parse_mode='Markdown'
            )
