from conf import API_URL, user_token
import requests
from datetime import datetime, timedelta
from conf import emoji


MAX_HUNGER = 288
MAX_WEARY  = 288

def hunger_to_str(temp: int) -> str:
  return {
       0               <= temp   < 0.25*MAX_HUNGER :  'Вы не думаете о еде',
       0.25*MAX_HUNGER <= temp   < 0.5*MAX_HUNGER  :  'Вы думаете, что пора поесть',
       0.5*MAX_HUNGER  <= temp   < 0.75*MAX_HUNGER :  'Вы испытываете сильный голод',
       0.75*MAX_HUNGER <= temp                     :  'Вы на грани смерти от истощения',
  }[True]

def weary_to_str(temp: int) -> str:
  return {
       0              <= temp   < 0.25*MAX_WEARY :  'Вы бодры и свежи',
       0.25*MAX_WEARY <= temp   < 0.5*MAX_WEARY  :  'Вы испытываете усталость',
       0.5*MAX_WEARY  <= temp   < 0.75*MAX_WEARY :  'Вы сильно утомлены',
       0.75*MAX_WEARY <= temp                    :  'Вы на грани срыва',
  }[True]


def person_status(U_ID):
    url = API_URL + '/person_status'
    req = requests.post(url, headers={'token' : user_token(U_ID) } )

    PERS = req.json()['person']
    STAT = req.json()['person_status']

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

