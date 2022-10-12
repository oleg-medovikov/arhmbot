from conf import API_URL, user_token
from clas import Manual
import requests


def update_manual(U_ID, df):
    url = API_URL + '/update_manual'
    
    head={'token' : user_token(U_ID)}
    
    MESS = ''
    
    for row in df.to_dict('records'):
        row.pop('date_update')
        
        try:
            M = Manual( **row )
        except Exception as e:
            MESS += str(e)
            return MESS
            
        req = requests.post(url, headers=head, json=M.__dict__ )
    
        if req.status_code == 200:
            MESS += req.json().get('mess') + '\n'
        else:
            continue

    return MESS

