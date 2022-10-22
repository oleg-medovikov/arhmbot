from conf import API_URL,  user_token
import requests


def make_get_event( U_ID ):
    url = API_URL + '/get_event'
    
    head={ 'token' : user_token(U_ID) }

    req = requests.get(url, headers=head  )
    
    if req.status_code == 200:
        return req.json()
    else:
        raise ValueError('Не удалось получить ивент')

