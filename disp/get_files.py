from .dispetcher import dp
from aiogram import types
import pandas as pd
import os

from func import delete_message, write_styling_excel
from conf import emoji
from clas import User, PersonDefaults, Location, \
    LocationDescription


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
    /test_emoji
    """.replace('_', '\\_')

    return await message.answer(MESS, parse_mode='Markdown')

DICT_XLSX = {
    'get_Events':             '/read_all_events',
    'get_Items':              '/read_all_items',
    'get_PersonDefaults':     '/read_all_persons_defaults',
    'get_Karta':              '/read_all_locations',
    'get_Manual':             '/read_full_manual',
    'get_Monsters':           '/read_all_monsters',
    'get_KartaDescriptions':  '/read_all_locations_descriptions',
        }


@dp.message_handler(commands=DICT_XLSX.keys())
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
async def send_full_emoji_dict(message :types.Message):
    # удалим команду для чистоты
    await delete_message(message)

    USER = await User.get(message['from']['id'])
    if USER is None or not USER.admin:
        return None


    MAX_LEN = max((len(k) + len(v)*0 for k,v in emoji.items() ))
    MESS = ''
    for key, value in emoji.items():
        word = key + ' '*(MAX_LEN - len(key))
        MESS += f'``` { word }   ```' + value +'\n'

    await message.answer( MESS, parse_mode='Markdown'  )
