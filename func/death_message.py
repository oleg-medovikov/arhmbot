from clas import Person, PersonStatus


def death_message(PERS: 'Person', PSTAT: 'PersonStatus') -> str:
    "Пишем эпитафию герою"

    date_reg = PERS.create_date.strftime('%d.%m.%Y в %H:%M')
    date_death = PERS.date_death.strftime('%d.%m.%Y в %H:%M')

    MESS = f"""```
===============================
     { PERS.gamename }
     { PERS.profession }
     { PERS.d_reason }
————- {date_reg} ——————-
       —————————————————
————- {date_death} ——————-

    По различным причинам
    приходят люди в Архэм,
    а остаются по одной...

    {'Его' if PERS.sex else 'Её'} светлой целью было:

    {PERS.destination}
===============================
```
"""

    return MESS
