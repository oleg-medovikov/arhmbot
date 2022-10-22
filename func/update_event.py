from conf import API_URL, user_token
from clas import Event
import requests


def update_event(U_ID, df):
    url = API_URL + '/update_event'
    
    head={'token' : user_token(U_ID)}
    
    MESS = ' '
    
    for row in df.to_dict('records'):
        row.pop('date_update')
        
        try:
            E = Event(**row)
        except Exception as e:
            MESS += str(e)
            return MESS
            
        print(E.__dict__)
        req = requests.post(url, headers=head, json=E.__dict__ )
    
        if req.status_code == 200:
            MESS += req.json().get('mess') + '\n'
        else:
            continue

    return MESS

