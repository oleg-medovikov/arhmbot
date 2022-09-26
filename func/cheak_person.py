from conf import API_URL, DICT_USERS_TOKENS
import requests


def cheak_person(U_ID):
    url = API_URL + '/cheak_person'

    req = requests.post(url, headers={'token' : DICT_USERS_TOKENS[str(U_ID)]  } )
    
    return req.json()

