from conf import API_URL, user_token
import requests


def get_locations_nearby( U_ID : int ) -> list:
    url = API_URL + '/locations_nearby'

    req = requests.get(url, headers={'token' : user_token( U_ID )} )
    
    if req.status_code == 200:
        return req.json()
    else:
        raise ValueError('Не удалось узнать локации по близости')

