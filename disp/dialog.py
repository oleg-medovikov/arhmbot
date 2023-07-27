from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text

from clas import Item, Dialog, DialogHistory
from func import update_message, create_keyboard
from conf import emoji


@dp.callback_query_handler(Text(startswith=['dialog_answer']))
async def dialog(query: types.CallbackQuery):
    "покупаем предмет в магазине"
    P_ID, S_ID, D_ID, Q_ID = [int(x) for x in query.data[14:].split('_')]

    DLOG = await Dialog.get(D_ID, Q_ID)
    DHIS = await DialogHistory.get(P_ID)
    DHIS.q_id = Q_ID
    DHIS.result = False
    DICT = dict()

    # сначала описываем возможные покупки
    for I_ID, COST in zip(DLOG.buy_items, DLOG.buy_costs):
        ITEM = await Item.get(I_ID)
        KEY = emoji(ITEM.emoji) + ' ' + ITEM.name + ' ' \
            + emoji('dollar') + ' ' + str(COST)
        DICT[KEY] = f'dialog_buy_{S_ID}_{D_ID}_{Q_ID}_{I_ID}_{COST}'

    # тут нужно повторить для возможных продаж
    for I_ID, COST in zip(DLOG.sale_items, DLOG.sale_costs):
        ITEM = await Item.get(I_ID)
        KEY = emoji(ITEM.emoji) + ' ' + ITEM.name + ' ' \
            + emoji('dollar') + ' ' + str(COST)
        DICT[KEY] = f'dialog_sale_{S_ID}_{I_ID}_{COST}'

    # теперь просто варианты ответов
    for KEY, ID in zip(DLOG.answers, DLOG.transfer):
        if ID == -1:
            # если есть ответ с выходом,
            # считаем диалог завершенным
            DICT[KEY] = 'continue_game'
            DHIS.result = True
            continue
        DICT[KEY] = f'dialog_answer_{P_ID}_{S_ID}_{D_ID}_{ID}'

    # обновляем историю диалога
    await DHIS.update()

    return await update_message(
            query.message,
            DLOG.description,
            create_keyboard(DICT)
                )
