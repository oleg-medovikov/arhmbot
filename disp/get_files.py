from .dispetcher import dp
from aiogram import types
import pandas as pd
import os, requests 
from func import write_styling_excel_file
from conf import DICT_USERS_TOKENS, API_URL 


@dp.message_handler(commands='get_PersonDefaults')
async def send_welcome(message: types.Message):
   # удалим команду для чистоты
    try:
        await message.delete()
    except:
        pass

    U_ID = message['from']['id']
    
    HEADERS = {
            'token' : DICT_USERS_TOKENS[str(U_ID)]
            }
    URL = API_URL + '/read_all_persons_defaults'

    req = requests.get(URL, headers=HEADERS)
    
    df = pd.DataFrame( data = req.json() )

    FILENAME = 'temp/PersonDefaults.xlsx'
    SHETNAME = 'def'

    write_styling_excel_file(FILENAME,df, SHETNAME)

    await message.answer_document(open(FILENAME, 'rb' ))
    os.remove(FILENAME)   

