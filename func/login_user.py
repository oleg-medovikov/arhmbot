from conf import API_URL, BOT_TOKEN, DICT_USERS_TOKENS
import requests


def login_user(U_ID):
    url = API_URL + '/login_user'

    req = requests.post(url, headers={'token' : BOT_TOKEN}, data=str(U_ID) )
    
    if 'token' in req.json():
        DICT_USERS_TOKENS [str(U_ID)] = req.json()['token']

    return 1

