from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text

from clas import PersonStatus, Shop, Item, Dialog, DialogHistory
from func import update_message, demand, create_keyboard
from conf import emoji


@dp.callback_query_handler(Text(startswith=['go_to_the_shop']))
async def go_to_the_shop(query: types.CallbackQuery):
    "Заходим в магазин"

    S_ID = int(query.data.split('_')[-1])

    SHOP = await Shop.get_by_id(S_ID)
    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])

    DICT = dict()

    if await demand(PERS, STAT, SHOP.get_demand()):
        # если персонаж проходит требования магазина
        MESS = SHOP.mess_welcome
        MESS += '\n\n' + f'У вас при себе  {emoji("dollar")} {STAT.money}'
        if SHOP.dialog:
            DIALOG = await Dialog.get(SHOP.dialog, 1)
            DICT[DIALOG.name] = f'dialog_answer_{S_ID}_{DIALOG.d_id}_1'
            # добавляем строчку о диалоге в историю
            await DialogHistory(**{
                'p_id':   STAT.p_id,
                's_id':   S_ID,
                'd_id':   DIALOG.d_id,
                'q_id':   1,
                'result': True,
                }).add()

        for ITEM in await Item.get_by_list(SHOP.product_list):
            LIST = (
                    emoji(ITEM.emoji), ' ',
                    ITEM.name,  '      ',
                    emoji('dollar'), ' ',
                    ITEM.cost,
                    )
            KEY = ''.join(str(x) for x in LIST)

            DICT[KEY] = f'dialog_buy_{S_ID}_{ITEM.i_id}_{ITEM.cost}'
        DICT['уйти'] = 'continue_game'
    else:
        # если не проходит требования
        MESS = SHOP.mess_not_pass
        DICT['понятно'] = 'continue_game'

    return await update_message(
            query.message,
            MESS,
            create_keyboard(DICT)
            )
