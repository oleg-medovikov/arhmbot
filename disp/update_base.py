from .dispetcher import dp, bot
from aiogram import types
import requests, os
from func import cheak_admin, update_person_defaults, update_location, update_location_description
import pandas as pd 

FILES = {
        'PersonDefaults.xlsx'    : 'update_person_defaults',
        'Karta.xlsx'             : 'update_location',
        'KartaDescriptions.xlsx' : 'update_location_description',
        }

NAMES = {
    'PersonDefaults.xlsx' : ['date_update', 'profession', 'start_location_id', 'money_min',
       'money_max', 'start_list_items', 'max_health_min', 'max_health_max',
       'max_mind_min', 'max_mind_max', 'speed_min', 'speed_max', 'stealth_min',
       'stealth_max', 'strength_min', 'strength_max', 'knowledge_min',
       'knowledge_max', 'godliness_min', 'godliness_max', 'luck_min',
       'luck_max'],
    'Karta': ['node_id', 'name_node', 'contact_list_id', 'district', 'street', 'dist',
       'date_update'],
    'KartaDescriptions' : ['node_id', 'stage', 'description', 'date_update']

        }

@dp.message_handler(content_types='document')
async def update_document(message : types.Message):
    """Работа с файлами которые посылает пользователь"""
    try:
        await message.delete()
    except:
        pass

    U_ID = message['from']['id']
    FILE = message['document']

    if not cheak_admin( U_ID ):
        return await message.answer('Зачем вы шлёте мне файлы?')

    if not FILE['file_name'] in FILES.keys():
        return await message.answer('У файла неправильное имя')

    DESTINATION = 'temp/' + FILE.file_unique_id + 'xlsx'

    await bot.download_file_by_id( 
            file_id= FILE.file_id,
            destination=DESTINATION)

    COLUMNS = NAMES.get( FILE['file_name'] )
    try:
        df = pd.read_excel(DESTINATION, usecols=COLUMNS)
    except Exception as e:
        await message.answer(str(e) )

    if   FILES.get( FILE['file_name'] ) == 'update_person_defaults':
        MESS = update_person_defaults(U_ID, df)    
        await message.answer( MESS )     
    elif FILES.get( FILE['file_name'] ) == 'update_location':
        MESS = update_location(U_ID, df )
        await message.answer( MESS )
    elif FILES.get( FILE['file_name'] ) == 'update_location_description':
        MESS = update_location_description(U_ID, df )
        await message.answer( MESS )

    os.remove(DESTINATION)



