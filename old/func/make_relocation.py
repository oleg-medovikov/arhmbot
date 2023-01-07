from conf import API_URL, user_token
import requests


def make_relocation( U_ID : int, NODE_ID : int ) -> tuple[str,bool]:
    url = API_URL + '/relocation'

    req = requests.post(url, headers={'token' : user_token( U_ID )}, data=str(NODE_ID) )
    
    if req.status_code == 200:
        return req.json()['MESS'], req.json()['die']
    else:
        raise ValueError(f'Не удалось сменить локацию  {NODE_ID}')

