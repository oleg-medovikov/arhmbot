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
        FIND_ITEM = 'ничего примечательного'
    else:
        ITEM = await Item.get(DP.i_id)
        FIND_ITEM = ITEM.name + '\n' + DP.comment

        # пробуем поместить предмет в сумку
        check, mess = await Inventory.add(PERS.p_id, ITEM.i_id)
        if check:
            await DP.delete_from_location()

        FIND_ITEM += '\n' + mess

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
        ).add(InlineKeyboardButton(
            text='продолжить', callback_data='continue_game'
            ))

    return await update_message(
        query.message,
        MESS,
        kb_look_around
            )
