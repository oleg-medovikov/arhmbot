from conf import API_URL,  user_token
import requests


def make_finish_event( U_ID: int, CHOICE : int ) -> tuple[bool,str]:
    url = API_URL + '/get_finish_event'
    
    head={ 'token' : user_token(U_ID) }

    req = requests.post(url, headers=head, data=str(CHOICE)  )
    
    if req.status_code == 200:
        return req.json()['error'], req.json()['MESS']
    else:
        raise ValueError('Не удалось закончить ивент')

