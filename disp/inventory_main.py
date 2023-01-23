from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from clas import User, Person, PersonStatus, Location, \
    LocationDescription, Item, DropItem, Inventory

DICT = {
    'HEAD': 'Непокрытая голова',
    'HAND_1': 'Пустая правая рука',
    'HAND_2': 'Пустая левая рука',
    'TWOHANDS': 'Пустые руки',
    'BODY': 'Голое тело',
    'LEGS': 'Голые ноги',
    'SHOES': 'Босые ноги',
    }


@dp.callback_query_handler(Text(equals=['inventory_main']))
async def inventory_main(query: types.CallbackQuery):
    "персонаж осматривается на местности и тратит время"
    # удаляем предыдущую клавиатуру
    await query.message.edit_reply_markup(reply_markup=None)
    U_ID = query.message['chat']['id']

    USER = await User.get(U_ID)
    PERSON = await Person.get(USER.u_id)
#    PERSTAT = await PersonStatus.get(PERSON)
#    LOCATION = await Location.get(PERSTAT.location)

    INV = await Inventory.get(PERSON.p_id)

    HEAD     = 'Пусто'
    HAND_1   = 'Пусто'
    HAND_2   = 'Пусто'
    TWOHANDS = 'Пусто'
    BODY     = 'Пусто'
    LEGS     = 'Пусто'

    for item in INV:
        if   item['slot'] == 'head':
            HEAD = item['emoji'] +' '+ item['name']
        elif item['slot'] == 'onehand':
            if HAND_1 == 'Пусто':
                HAND_1 = item['emoji'] +' '+ item['name']
            else:
                HAND_2 = item['emoji'] +' '+ item['name']
        elif item['slot'] == 'twohands':
            TWOHANDS = item['emoji'] +' '+ item['name']
        elif item['slot'] == 'BODY':
            BODY = item['emoji'] +' '+ item['name']
        elif item['slot'] == 'legs':
            LEGS = item['emoji'] +' '+ item['name']

    if TWOHANDS != 'Пусто':
        RUKI = 'В руках: ' + TWOHANDS
    else:
        RUKI = f"""
В правой руке: {HAND_1}
В левой  руке: {HAND_2}
"""

    MESS = f"""```
Ваш инвентарь, {PERSON.gamename}
__________________________
Голова: {HEAD}
{RUKI}
Тело: {BODY}
Ноги: {LEGS}
В вашей сумке:
```
"""
