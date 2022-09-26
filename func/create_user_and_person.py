import requests 
from conf import API_URL, BOT_TOKEN

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

    header = {
            'token' : BOT_TOKEN
            }

    body = {
        "u_id"        : U_ID,
        "gamename"    : gamename,
        "sex"         : s,
        "profession"  : profession,
        "destination" : destination    
            }

    req = requests.post(url, headers=header, json=body)

    
