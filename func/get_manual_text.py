from conf import API_URL,  user_token
import requests


def get_manual_text(U_ID, M_ID ):
    url = API_URL + '/get_manual_text'
    
    head={ 'token' : user_token(U_ID) }

    req = requests.get(url, headers=head , data=str( M_ID)   )
    
    if req.status_code == 200:
        return req.json()
    else:
        raise ValueError('Не удалось прочесть мануал')

