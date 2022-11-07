from conf import API_URL, user_token
import requests


def check_person(U_ID):
    url = API_URL + '/check_person'

    req = requests.post(url, headers={'token' : user_token(U_ID)  } )
    
    return req.json()

