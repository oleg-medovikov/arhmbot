from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from clas import PersonStatus, Inventory, String
from func import update_message
from conf import emoji


@dp.callback_query_handler(Text(startswith=['dialog_buy_']))
async def buy_item(query: types.CallbackQuery):
    "покупаем предмет в магазине"
    print(query.data)
    # стоимость
    COST = int(query.data.split('_')[-1])
    # предмет
    I_ID = int(query.data.split('_')[-2])
    # магазин
    S_ID = int(query.data.split('_')[-3])

    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])

    kb_shop = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )
    # проверяем, достаточно ли денег у персонажа
    if STAT.money < COST:
        MESS = emoji('8leg') + '   ' + await String.get('not_enough_money')
        kb_shop.add(InlineKeyboardButton(
            text='Понимаю',
            callback_data=f'go_to_the_shop_{S_ID}'
            ))
        return await update_message(
            query.message,
            MESS,
            kb_shop
                )

    INV = await Inventory.get(PERS)
    CHECK, STRING = await INV.add(I_ID)
    if CHECK:
        # удачная покупка
        STAT.money -= COST
        await STAT.update()

    MESS = emoji('8leg') + '   ' + STRING
    kb_shop.add(InlineKeyboardButton(
        text='Понимаю',
        callback_data=f'go_to_the_shop_{S_ID}'
        ))
    return await update_message(
        query.message,
        MESS,
        kb_shop
            )
