from .dispetcher import dp
from aiogram import types
import pandas as pd
import os, requests 
from func import cheak_admin, write_styling_excel_file
from conf import API_URL, user_token, emoji

@dp.message_handler(commands='files')
async def get_files_help(message: types.Message):
    try:
        await message.delete()
    except: pass
    
    if not cheak_admin( message['from']['id'] ): return None

    MESS = """*Доступные команды для редактирования базы*
    
    /get_PersonDefaults
    /get_Karta
    /get_KartaDescriptions
    /get_Manual
    /get_Items
    /get_Events
    /test_emoji

    """.replace('_', '\\_')
    
    return await message.answer(MESS, parse_mode='Markdown')

DICT_XLSX = {
    'get_Events'            : '/read_all_events',
    'get_Items'             : '/read_all_items',
    'get_PersonDefaults'    : '/read_all_persons_defaults',
    'get_Karta'             : '/read_all_locations',
    'get_Manual'            : '/read_full_manual',
    'get_KartaDescriptions' : '/read_all_locations_descriptions',

        }

@dp.message_handler(commands= DICT_XLSX.keys() )
async def send_objects_file(message: types.Message):
   # удалим команду для чистоты
    try:
        await message.delete()
    except: pass

    COMMAND = message.text.replace('/', '')
    U_ID = message['from']['id']

    URL = API_URL + str( DICT_XLSX.get(COMMAND) )
    req = requests.get(URL, headers={'token' : user_token(U_ID)})
    
    df = pd.DataFrame( data = req.json() )
    df['date_update'] = pd.to_datetime(df['date_update']).dt.strftime('%H:%M  %d.%m.%Y')
    FILENAME = f'temp/{COMMAND[4:]}.xlsx'
    SHETNAME = 'def'

    write_styling_excel_file(FILENAME,df, SHETNAME)

    await message.answer_document(open(FILENAME, 'rb' ))
    os.remove(FILENAME)   

@dp.message_handler(commands='test_emoji')
async def send_full_emoji_dict(message :types.Message):
    # удалим команду для чистоты
    try:
        await message.delete()
    except: pass

    MAX_LEN = max((len(k) + len(v)*0 for k,v in emoji.items() ))
    MESS = ''
    for key, value in emoji.items():
        word = key + ' '*(MAX_LEN - len(key))
        MESS += f'``` { word }   ```' + value +'\n'

    await message.answer( MESS, parse_mode='Markdown'  )
