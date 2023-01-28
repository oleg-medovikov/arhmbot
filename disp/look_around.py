from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from clas import PersonStatus, Location, \
    LocationDescription, Item, DropItem, Inventory
from func import update_message


@dp.callback_query_handler(Text(equals=['look_around']))
async def look_around(query: types.CallbackQuery):
    "персонаж осматривается на местности и тратит время"

    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])

    LOCATION = await Location.get(STAT.location)

    await STAT.waste_time(1)

    DESCR_loc = await LocationDescription.get(
                    LOCATION.node_id,
                    STAT.stage
                    )
    DESCR_dist = await LocationDescription.get(
                    LOCATION.district_id,
                    STAT.stage
                    )
    LOCATION.district = LOCATION.district.replace(' район', '')
    p_1 = '-'*(len(LOCATION.district) + 6)
    p_2 = '-'*len(LOCATION.name_node)

    # пробуем найти на локации предметы
    try:
        DP = await DropItem.get(LOCATION.node_id, STAT.stage)
    except ValueError:
        FIND = False
        FIND_ITEM = 'ничего примечательного'
    else:
        FIND = True
        ITEM = await Item.get(DP.i_id)
        FIND_ITEM = ITEM.name + '\n\n' + DP.comment

    # Формируем сообщение

    FIND_ = 'Осмотревшись Вы обнаружили'
    LIST = (
        '``` \n',
        'Район ', LOCATION.district,
        '\n', p_1, '\n',
        DESCR_dist, '\n\n',
        LOCATION.name_node,
        '\n', p_2, '\n',
        DESCR_loc,
        '\n\n', FIND_,  '\n',
        '-'*len(FIND_), '\n',
        FIND_ITEM,
        '\n ``` \n',
            )

    MESS = ''.join(str(x) for x in LIST)

    kb_look_around = InlineKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
        )

    # если игрок нашёл предмет, то предложить его поднять
    if FIND:
        DICT = {
            'Подобрать предмет':    f'look_around_get_{DP.di_id}',
            'Оставить предмет в покое': 'continue_game',
            }
    else:
        DICT = {
            'Продолжить': 'continue_game'
                }

    for key, value in DICT.items():
        kb_look_around.add(InlineKeyboardButton(
            text=key,
            callback_data=value
            ))

    return await update_message(
        query.message,
        MESS,
        kb_look_around
            )


@dp.callback_query_handler(Text(startswith=['look_around_get_']))
async def look_around_get_item(query: types.CallbackQuery):
    "игрок захотел поднять предмет"

    DI_ID = int(query.data.split('_')[-1])

    try:
        DP = await DropItem.get_by_id(DI_ID)
    except ValueError:
        MESS = 'Вы нагнулись за предметом, но кто-то выхватил его быстрее!'
        GET = False
    else:
        GET = True
        PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])

    # пробуем поместить предмет в сумку
    if GET:
        check, MESS = await Inventory.add(PERS.p_id, DP.i_id)
        if check:
            await DP.delete_from_location()

    DICT = {
            'Продолжить': 'continue_game'
        }

    kb_look_around = InlineKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
        )

    for key, value in DICT.items():
        kb_look_around.add(InlineKeyboardButton(
            text=key,
            callback_data=value
            ))

    return await update_message(
        query.message,
        MESS,
        kb_look_around
            )
