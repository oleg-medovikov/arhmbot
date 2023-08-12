from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text

from clas import PersonStatus, Inventory, String
from func import update_message, create_keyboard
from conf import emoji


@dp.callback_query_handler(Text(startswith=['dialog_buy_']))
async def dialog_buy_item(query: types.CallbackQuery):
    "покупаем предмет в магазине"

    S_ID, D_ID, Q_ID, I_ID, COST = [int(x) for x in query.data[11:].split('_')]

    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])
    DICT = {}
    # проверяем, достаточно ли денег у персонажа
    if STAT.money < COST:
        MESS = emoji('8leg') + '   ' + await String.get('not_enough_money')
        DICT['Понимаю'] = f'go_to_the_shop_{S_ID}'

        return await update_message(
            query.message,
            MESS,
            create_keyboard(DICT)
            )

    INV = await Inventory.get(PERS)
    CHECK, STRING = await INV.add(I_ID)
    if CHECK:
        # удачная покупка
        STAT.money -= COST
        await STAT.update()

    MESS = emoji('8leg') + '   ' + STRING
    DICT['Понимаю'] = f'dialog_answer_{PERS.p_id}_{S_ID}_{D_ID}_{Q_ID}'

    return await update_message(
        query.message,
        MESS,
        create_keyboard(DICT)
        )
