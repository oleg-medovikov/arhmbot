from clas import Person, PersonStatus


def death_message(PERSON: 'Person', PSTAT: 'PersonStatus') -> str:
    "Пишем эпитафию герою"

    date_reg = PERSON.create_date.strftime('%d.%m.%Y в %H:%M')
    date_death = PERSON.date_death.strftime('%d.%m.%Y в %H:%M')

    MESS = f"""```
===============================
     { PERSON.gamename }
     { PERSON.profession }
     { PERSON.d_reason }
————- {date_reg} ——————-
       —————————————————
————- {date_death} ——————-

    По различным причинам
    приходят люди в Архэм,
    а остаются по одной...

    {'Его' if PERSON.sex else 'Её'} светлой целью было:

    {PERSON.destination}
===============================
```
"""

    return MESS
