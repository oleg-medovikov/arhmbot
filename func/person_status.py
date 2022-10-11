from conf import API_URL, user_token
import requests
from datetime import datetime, timedelta
from conf import emoji


def hunger_to_str(temp: int) -> str:
    return {
         0   <= temp   < 4  :  'Сытый        ',
         4   <= temp   < 6  :  'Пора поесть  ',
         6   <= temp   < 8  :  'Сильный голод',
         8   <= temp   < 10 :  'При смерти   ',
    }[True]

def weary_to_str(temp: int) -> str:
    return {
         0   <= temp   < 4  :  'Свеж и бодр      ',
         4   <= temp   < 6  :  'Усталость        ',
         6   <= temp   < 8  :  'Сильное утомление',
         8   <= temp   < 10 :  'При смерти       ',
    }[True]




def person_status(U_ID):
    url = API_URL + '/person_status'

    req = requests.post(url, headers={'token' : user_token(U_ID) } )
    
    
    PERS = req.json()['person']
    STAT = req.json()['person_status']
    # 'hunger': 0, 'weary': 0
    
    print(PERS, STAT)

    DATE = datetime.fromisoformat(PERS['create_date']).strftime('%d.%m.%Y в %H:%M')
    DAYS = STAT['gametime'] // 96 
    TIME = (datetime.strptime('09:00', '%H:%M') + timedelta(minutes=15*STAT['gametime'])).strftime('%H:%M')


    MESS=f"""*Карточка персонажа*

*ИМЯ:* {PERS['gamename']},  {PERS['profession']}
*Зарегистрирован: * {DATE}
*Провел дней в Архэме: {DAYS}*  
```

  {emoji['clock']}  {TIME}    {emoji['dollar']} {STAT['money']}

  {emoji['heart']} {STAT['health']} из {PERS['max_health']}    {emoji['brain']} {STAT['mind']} из {PERS['max_mind']}

  {emoji['strength']} {STAT['strength']}    {emoji['speed']} {STAT['speed']}    {emoji['stealth']} {STAT['stealth']}  

  {emoji['knowledge']} {STAT['knowledge']}    {emoji['godliness']} {STAT['godliness']}    {emoji['luck']} {STAT['luck']}  

  {emoji['hunger']} {hunger_to_str(STAT['hunger'])}

  {emoji['weary']} {weary_to_str(STAT['weary'])}
```
*Достижения:*
```
  нет
```
"""




    return MESS

