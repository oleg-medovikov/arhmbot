from conf import API_URL, user_token
from clas import Monster
import requests


def update_monster(U_ID, df):
    url = API_URL + '/update_monster'
    
    head={'token' : user_token(U_ID)}
    
    MESS = ' '
    
    for row in df.to_dict('records'):
        row.pop('date_update')
        
        try:
            M = Monster(**row)
        except Exception as e:
            MESS += str(e)
            return MESS
            
        req = requests.post(url, headers=head, json=M.__dict__ )
    
        if req.status_code == 200:
            if 'исправлена' in req.json().get('mess') or \
                    'добавлена' in req.json().get('mess'):
                MESS += req.json().get('mess') + '\n'
        else:
            continue

    if MESS == ' ':
        MESS = 'без изменений'

    return MESS

