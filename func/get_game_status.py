from conf import API_URL, user_token
import requests


def get_game_status( U_ID : int ) -> str:
    url = API_URL + '/get_game_status'

    req = requests.get(url, headers={'token' : user_token( U_ID )} )
    
    if req.status_code == 200:
        return req.json()['MESS']
    else:
        raise ValueError('Не удалось узнать гейм статус')

