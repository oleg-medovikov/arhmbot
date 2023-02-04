from .dispetcher import dp
from aiogram import types
import pandas as pd
import os

from func import delete_message, write_styling_excel
from conf import emoji, emoji_all
from clas import User, PersonDefaults, Location, \
    LocationDescription, Manual, Item, Event, \
    Monster, String, Shop


@dp.message_handler(commands='files')
async def get_files_help(message: types.Message):
    await delete_message(message)

    USER = await User.get(message['from']['id'])
    if USER is None or not USER.admin:
        return None

    MESS = """*Доступные команды для редактирования базы*

    /get_PersonDefaults
    /get_Karta
    /get_KartaDescriptions
    /get_Manual
    /get_Items
    /get_Events
    /get_Monsters
    /get_Strings
    /get_Shops
    /test_emoji
    """.replace('_', '\\_')

    return await message.answer(MESS, parse_mode='Markdown')

DICT_XLSX = [
    'get_Events',
    'get_Items',
    'get_PersonDefaults',
    'get_Karta',
    'get_Manual',
    'get_Monsters',
    'get_KartaDescriptions',
    'get_Strings',
    'get_Shops',
    ]


@dp.message_handler(commands=DICT_XLSX)
async def send_objects_file(message: types.Message):
    # удалим команду для чистоты
    await delete_message(message)

    USER = await User.get(message['from']['id'])
    if USER is None or not USER.admin:
        return None

    COMMAND = message.text.replace('/', '')

    JSON = {
        'get_PersonDefaults':    PersonDefaults.get_all(),
        'get_Karta':             Location.get_all(),
        'get_KartaDescriptions': LocationDescription.get_all(),
        'get_Manual':            Manual.get_all(),
        'get_Items':             Item.get_all(),
        'get_Events':            Event.get_all(),
        'get_Monsters':          Monster.get_all(),
        'get_Strings':           String.get_all(),
        'get_Shops':             Shop.get_all(),
        }.get(COMMAND)

    try:
        JSON = await JSON
    except TypeError:
        return await message.answer('Пока проблемы с этой командой')

    df = pd.DataFrame(data=JSON)
    df['date_update'] = df['date_update'].dt.strftime('%H:%M  %d.%m.%Y')
    FILENAME = f'temp/{COMMAND[4:]}.xlsx'
    SHETNAME = 'def'

    write_styling_excel(FILENAME, df, SHETNAME)

    await message.answer_document(open(FILENAME, 'rb'))
    os.remove(FILENAME)


@dp.message_handler(commands='test_emoji')
async def send_full_emoji_dict(message: types.Message):
    # удалим команду для чистоты
    await delete_message(message)

    USER = await User.get(message['from']['id'])
    if USER is None or not USER.admin:
        return None

    MAX_LEN = max((len(k) for k in emoji_all()))
    MESS = ''
    for key in emoji_all():
        word = key + ' '*(MAX_LEN - len(key))
        MESS += f'``` { word }   ```' + emoji(key) + '\n'

    await message.answer(MESS, parse_mode='Markdown')
