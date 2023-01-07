from conf import API_URL, BOT_TOKEN, user_token
import requests


def make_admin(U_ID):
    url = API_URL + '/make_admin'
    
    head={'token1' : BOT_TOKEN,
          'token2' : user_token(U_ID)}

    req = requests.post(url, headers=head )
    
    if req.status_code == 200:
        return True
    else:
        return False

