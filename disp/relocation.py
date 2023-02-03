from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from clas import PersonStatus, Location
from func import update_message, timedelta_to_str
from conf import emoji

@dp.callback_query_handler(Text(equals='leave'))
async def leave(query: types.CallbackQuery):
    "проверить список локаций по близости и предложить игроку"
    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])

    LOCATIONS = await Location.nearby(STAT.location)

    kb_loc_nearby = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )

    for loc in LOCATIONS:
        kb_loc_nearby.add(InlineKeyboardButton(
            text=loc['name_node'],
            callback_data='leave_' + str(loc['node_id'])
            ))
    kb_loc_nearby.add(InlineKeyboardButton(
        text='остаться на месте',
        callback_data='continue_game'
        ))

    MESS = 'Вы можете пойти:'

    return await update_message(
            query.message,
            MESS,
            kb_loc_nearby
            )


@dp.callback_query_handler(Text(startswith='leave_'))
async def relocation(query: types.CallbackQuery):
    NODE_ID = int(query.data.split('_')[-1])

    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])

    WASTE = await STAT.waste_time(1)

    STAT.location = NODE_ID

    await STAT.update()

    LOCATION = await Location.get(STAT.location)

    LIST_1 = (
        'Вы отдали последние силы,\n',
        'чтобы оказаться ', LOCATION.declension, ',\n',
        'но их не хватило...',
            )
    LIST_2 = (
        'Вы отдали последние силы,\n',
        'чтобы оказаться ', LOCATION.declension, ',\n',
        'но их не хватило...',
            )
    LIST_3 = (
        emoji('stopwatch'), ' ', timedelta_to_str(WASTE), '\n\n',
        'Вы оказались ', LOCATION.declension, ',\n',
        'хотите идти дальше?',
            )

    LIST, DIE = {
        STAT.mind < 1:   (LIST_1, True),
        STAT.health < 1: (LIST_2, True),
        }.get(True, (LIST_3, False))

    MESS = ''.join(str(x) for x in LIST)

    kb_relocation = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )

    # Если персонаж не умер, можно идти дальше
    if not DIE:
        kb_relocation.add(InlineKeyboardButton(
                text='идти дальше', callback_data='leave'
                ))

    # в любом случае предлагаем продолжить
    kb_relocation.add(InlineKeyboardButton(
                text='остановиться', callback_data='continue_game'
                ))

    return await update_message(
            query.message,
            MESS,
            kb_relocation
            )
