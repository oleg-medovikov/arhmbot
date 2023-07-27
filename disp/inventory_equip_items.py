from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text

from clas import PersonStatus, Inventory

from func import inventory_mess, update_message, create_keyboard
from conf import emoji

equip_slots = [
    'head', 'earrings', 'hands', 'rings',
    'body', 'legs', 'shoes'
    ]


@dp.callback_query_handler(Text(equals=['inventory_equip_items']))
async def inventory_equip_items(query: types.CallbackQuery):
    "показываем игроку список надетых вещей"
    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])

    INVE = await Inventory.get(PERS)
    ITEMS = await INVE.get_all()

    MESS = inventory_mess(PERS, ITEMS, EQUIP=True)
    DICT = {}

    for slot in equip_slots:
        for item in ITEMS[slot]:
            KEY = emoji(item['emoji']) + ' ' + item['name']
            VALUE = 'inventory_equip_item_' + str(item['i_id'])
            DICT[KEY] = VALUE
    DICT['назад'] = 'inventory_main'
    return await update_message(
            query.message,
            MESS,
            create_keyboard(DICT)
    )
