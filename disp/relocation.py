from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from clas import User, Person, PersonStatus, Location


@dp.callback_query_handler(Text(equals='leave'))
async def leave(query: types.CallbackQuery):
    "проверить список локаций по близости и предложить игроку"
    # удаляем предыдущую клавиатуру
    await query.message.edit_reply_markup(reply_markup=None)
    U_ID = query.message['chat']['id']

    USER = await User.get(U_ID)
    PERSON = await Person.get(USER.u_id)
    PERSTAT = await PersonStatus.get(PERSON)

    LOCATIONS = await Location.nearby(PERSTAT.location)

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

    await query.message.answer(MESS, reply_markup=kb_loc_nearby)


@dp.callback_query_handler(Text(startswith='leave_'))
async def relocation(query: types.CallbackQuery):
    NODE_ID = query.data.split('_')[-1]
    U_ID = query.message['chat']['id']

    USER = await User.get(U_ID)
    PERSON = await Person.get(USER.u_id)
    PERSTAT = await PersonStatus.get(PERSON)

    await PERSTAT.waste_time(1)

    PERSTAT.location = int(NODE_ID)

    await PERSTAT.update()

    LOCATION = await Location.get(PERSTAT.location)

    PERSTAT = await PersonStatus.get(PERSON)

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
        'Прошло какое-то время,\n',
        'и Вы оказались ', LOCATION.declension, ',\n',
        'хотите идти дальше?',
            )

    LIST, DIE = {
        PERSTAT.mind < 1:   (LIST_1, True),
        PERSTAT.health < 1: (LIST_2, True),
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

    await query.message.answer(MESS, reply_markup=kb_relocation)
