from conf import API_URL, user_token
from clas import Item
import requests


def update_item(U_ID, df):
    url = API_URL + '/update_item'
    
    head={'token' : user_token(U_ID)}
    
    MESS = ' '
    
    for row in df.to_dict('records'):
        row.pop('date_update')
        
        try:
            I = Item(**row)
        except Exception as e:
            MESS += str(e)
            return MESS
            
        req = requests.post(url, headers=head, json=I.__dict__ )
    
        if req.status_code == 200:
            MESS += req.json().get('mess') + '\n'
        else:
            continue

    return MESS

