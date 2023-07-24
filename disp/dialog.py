from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from clas import Item, Dialog
from func import update_message
from conf import emoji


@dp.callback_query_handler(Text(startswith=['dialog_answer']))
async def dialog(query: types.CallbackQuery):
    "покупаем предмет в магазине"
    Q_ID = int(query.data.split('_')[-1])
    D_ID = int(query.data.split('_')[-2])
    S_ID = int(query.data.split('_')[-3])

    kb_dialog = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )

    DLOG = await Dialog.get(D_ID, Q_ID)

    DICT = dict()

    # сначала описываем возможные покупки
    for I_ID, COST in zip(DLOG.buy_items, DLOG.buy_costs):
        ITEM = await Item.get(I_ID)
        KEY = emoji(ITEM.emoji) + ' ' + ITEM.name + ' ' \
            + emoji('dollar') + ' ' + str(COST)
        DICT[KEY] = f'dialog_buy_{S_ID}_{I_ID}_{COST}'
        print(DICT[KEY])

    # тут нужно повторить для возможных продаж
    for I_ID, COST in zip(DLOG.sale_items, DLOG.sale_costs):
        ITEM = await Item.get(I_ID)
        KEY = emoji(ITEM.emoji) + ' ' + ITEM.name + ' ' \
            + emoji('dollar') + ' ' + str(COST)
        DICT[KEY] = f'dialog_sale_{S_ID}_{I_ID}_{COST}'

    # теперь просто варианты ответов
    for KEY, ID in zip(DLOG.answers, DLOG.transfer):
        DICT[KEY] = f'dialog_answer_{S_ID}_{D_ID}_{ID}' if ID != -1 \
            else 'continue_game'

    for key, value in DICT.items():
        kb_dialog.add(InlineKeyboardButton(
            text=key,
            callback_data=value
            ))

    return await update_message(
            query.message,
            DLOG.description,
            kb_dialog
                )
