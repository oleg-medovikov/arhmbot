from conf import API_URL,  user_token
import requests


def get_inventory( U_ID ):
    url = API_URL + '/get_inventory'
    
    head={ 'token' : user_token(U_ID) }

    req = requests.get(url, headers=head )
    
    if req.status_code == 200:
        return req.json()['MESS'], req.json()['INV']
    else:
        raise ValueError('Не удалось получить инвентарь')

