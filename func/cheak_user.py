from conf import API_URL
import requests


def cheak_user(U_ID):
    url = API_URL + '/cheak_user'
    data = {
            'username' : str(U_ID)
            }
    req = requests.post(url, data=data )
    
    return req.json()

