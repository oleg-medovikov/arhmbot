import requests 
from conf import SALT, API_URL

def create_user_and_person(
        U_ID : int,
        gamename : str,
        sex : str,
        profession  : str,
        destination : str
        ):
    url = API_URL + '/create_user_from_bot'

    if sex == 'male' : s = True
    else: s = False

    body = {
        "u_id"        : U_ID,
        "gamename"    : gamename,
        "sex"         : s,
        "profession"  : profession,
        "destination" : destination    
            }

    req = requests.post(url, headers={'salt' : SALT}, json=body)

    
