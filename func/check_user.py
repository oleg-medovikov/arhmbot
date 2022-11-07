from conf import API_URL, BOT_TOKEN
import requests


def check_user(U_ID):
    url = API_URL + '/check_user'

    req = requests.post(url, headers={'token' : BOT_TOKEN}, data=str(U_ID) )
    
    if req.status_code == 200:
        return req.json()

