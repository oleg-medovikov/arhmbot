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
    /test_emoji

    """.replace('_', '\\_')
    
    return await message.answer(MESS, parse_mode='Markdown')

@dp.message_handler(commands='get_PersonDefaults')
async def send_PersonDefaults_file(message: types.Message):
   # удалим команду для чистоты
    try:
        await message.delete()
    except: pass

    U_ID = message['from']['id']
    
    URL = API_URL + '/read_all_persons_defaults'

    req = requests.get(URL, headers={'token' : user_token(U_ID)})
    
    df = pd.DataFrame( data = req.json() )
    
    df['date_update'] = pd.to_datetime(df['date_update']).dt.strftime('%H:%M  %d.%m.%Y')
    FILENAME = 'temp/PersonDefaults.xlsx'
    SHETNAME = 'def'

    write_styling_excel_file(FILENAME,df, SHETNAME)

    await message.answer_document(open(FILENAME, 'rb' ))
    os.remove(FILENAME)   

@dp.message_handler(commands='get_Karta')
async def send_Karta_file(message: types.Message):
   # удалим команду для чистоты
    try:
        await message.delete()
    except: pass

    U_ID = message['from']['id']
    URL = API_URL + '/read_all_locations'
    req = requests.get(URL, headers={'token' : user_token(U_ID)})
    
    df = pd.DataFrame( data = req.json() )
    if len(df) == 0:
        return await message.answer('Таблица пуста')
    
    df['date_update'] = pd.to_datetime(df['date_update']).dt.strftime('%H:%M  %d.%m.%Y')
    FILENAME = 'temp/Karta.xlsx'
    SHETNAME = 'def'

    write_styling_excel_file(FILENAME,df, SHETNAME)

    await message.answer_document(open(FILENAME, 'rb' ))
    os.remove(FILENAME)   

@dp.message_handler(commands='get_KartaDescriptions')
async def send_Karta_Descriptions_file(message: types.Message):
   # удалим команду для чистоты
    try:
        await message.delete()
    except: pass

    U_ID = message['from']['id']
    URL = API_URL + '/read_all_locations_descriptions'
    req = requests.get(URL, headers={'token' : user_token(U_ID)})
    
    df = pd.DataFrame( data = req.json() )
    if len(df) == 0:
        return await message.answer('Таблица пуста')
    
    df['date_update'] = pd.to_datetime(df['date_update']).dt.strftime('%H:%M  %d.%m.%Y')
    FILENAME = 'temp/KartaDescriptions.xlsx'
    SHETNAME = 'def'

    write_styling_excel_file(FILENAME,df, SHETNAME)

    await message.answer_document(open(FILENAME, 'rb' ))
    os.remove(FILENAME)   

@dp.message_handler(commands='get_Manual')
async def send_Manual_file(message: types.Message):
   # удалим команду для чистоты
    try:
        await message.delete()
    except: pass

    U_ID = message['from']['id']
    URL = API_URL + '/read_full_manual'
    req = requests.get(URL, headers={'token' : user_token(U_ID)})
    
    df = pd.DataFrame( data = req.json() )
    if len(df) == 0:
        return await message.answer('Таблица пуста')
    
    df['date_update'] = pd.to_datetime(df['date_update']).dt.strftime('%H:%M  %d.%m.%Y')
    FILENAME = 'temp/Manual.xlsx'
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
