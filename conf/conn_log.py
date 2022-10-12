
from .config import API_URL, BOT_TOKEN
import requests


def login_user(U_ID):
    url = API_URL + '/login_user'

    req = requests.post(url, headers={'token' : BOT_TOKEN}, data=str(U_ID) )
    
    if 'token' in req.json():
        return req.json().get('token')
    else:
        raise ValueError('не удалось залогиниться')



DICT_USERS_TOKENS = dict()

def user_token(u_id : int) -> str:
    ID = str(u_id) 
    if ID in DICT_USERS_TOKENS.keys():
        TOKEN = DICT_USERS_TOKENS.get( ID )
        return str(TOKEN)
    else:
        TOKEN = login_user(u_id)
        DICT_USERS_TOKENS[ ID ] = TOKEN
        return TOKEN
