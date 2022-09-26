from conf import API_URL, DICT_USERS_TOKENS
import requests
from datetime import datetime, timedelta
from conf import emoji

def person_status(U_ID):
    url = API_URL + '/person_status'

    req = requests.post(url, headers={'token' : DICT_USERS_TOKENS[str(U_ID)]  } )
    
    
    PERS = req.json()['person']
    STAT = req.json()['person_status']
    print(STAT)
    DATE = datetime.fromisoformat(PERS['create_date']).strftime('%d.%m.%Y в %H:%M')
    DAYS = STAT['gametime'] // 96 
    TIME = (datetime.strptime('09:00', '%H:%M') + timedelta(minutes=15*STAT['gametime'])).strftime('%H:%M')
    MESS=f"""*Карточка персонажа*

*ИМЯ:* {PERS['gamename']},  {PERS['profession']}
*Зарегистрирован: * {DATE}
*Провел дней в Архэме: {DAYS}*  

{emoji['clock']}  {TIME}  {emoji['dollar']} {STAT['money']}

{emoji['heart']} {STAT['health']} из {PERS['max_health']}    {emoji['brain']} {STAT['mind']} из {PERS['max_mind']}

|  {emoji['strength']} {STAT['strength']}  |  {emoji['speed']} {STAT['speed']}  |  {emoji['stealth']} {STAT['stealth']}  |

|  {emoji['knowledge']} {STAT['knowledge']}  |  {emoji['godliness']} {STAT['godliness']}  |  {emoji['luck']} {STAT['luck']}  |

"""




    return MESS

