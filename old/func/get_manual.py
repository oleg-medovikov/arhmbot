from conf import API_URL,  user_token
import requests


def get_manual(U_ID):
    url = API_URL + '/read_full_manual'
    
    head={ 'token' : user_token(U_ID) }

    req = requests.get(url, headers=head )
    
    if req.status_code == 200:
        return req.json()
    else:
        raise ValueError('Не удалось прочесть мануал')

