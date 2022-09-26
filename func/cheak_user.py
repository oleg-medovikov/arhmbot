from conf import API_URL, BOT_TOKEN
import requests


def cheak_user(U_ID):
    url = API_URL + '/cheak_user'

    req = requests.post(url, headers={'token' : BOT_TOKEN}, data=str(U_ID) )
    
    return req.json()

