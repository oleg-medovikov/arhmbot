from conf import API_URL, user_token
from clas import LocationDescription
import requests


def update_location_description(U_ID, df):
    url = API_URL + '/update_location_description'
    
    head={'token' : user_token(U_ID)}
    
    MESS = ''
    
    for row in df.to_dict('records'):
        row.pop('date_update')
        try:
            PD = LocationDescription(**row)
        except Exception as e:
            MESS += str(e)
            return MESS

        req = requests.post(url, headers=head, json=PD.__dict__ )
    
        if req.status_code == 200:
            MESS += req.json().get('mess') + '\n'
        else:
            continue

    return MESS

