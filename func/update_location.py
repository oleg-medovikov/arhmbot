from pandas.core.arrays import ExtensionArray
from conf import API_URL, user_token
from clas import Location
import requests


def update_location(U_ID, df):
    url = API_URL + '/update_location'
    
    head={'token' : user_token(U_ID)}
    
    MESS = ''
    
    for row in df.to_dict('records'):
        row.pop('date_update')
        
        try:
            LOC = Location(**row)
        except Exception as e:
            MESS += str(e)
            return MESS
            
        req = requests.post(url, headers=head, json=LOC.__dict__ )
    
        if req.status_code == 200:
            MESS += req.json().get('mess') + '\n'
        else:
            continue

    return MESS

