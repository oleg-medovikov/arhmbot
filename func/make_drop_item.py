import requests
from conf import user_token, API_URL


def make_drop_item(U_ID : int, I_ID : int) -> str:
    url = API_URL + '/make_drop_item'
    
    head={'token' : user_token(U_ID)}
    
    req = requests.post(url, headers=head, data=str(I_ID) )
    
    if req.status_code == 200:
        return  req.json().get('MESS') 
    else:
        ValueError('Не удалось использовать предмет')
 
