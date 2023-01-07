from conf import API_URL,  user_token
import requests


def get_item( U_ID, I_ID ):
    url = API_URL + '/get_item'
    
    head={ 'token' : user_token(U_ID) }

    req = requests.post(url, headers=head, data=str(I_ID)  )
    
    if req.status_code == 200:
        return req.json()
    else:
        raise ValueError('Не удалось получить инвентарь')

