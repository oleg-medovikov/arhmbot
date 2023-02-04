from datetime import datetime, timedelta

from clas import Person, PersonStatus, Inventory


async def demand(PERS: 'Person', STAT: 'PersonStatus', DEMAND: dict) -> bool:
    "Прохождение проверки персонажем"
    for key, value in DEMAND.items():
        if key in ('sex', 'profession'):
            # Это проверка персоны
            if PERS.dict()[key] != value:
                return False

        if key in (
            'money', 'health', 'mind', 'speed',
            'stealth', 'strength', 'knowledge',
            'godliness', 'luck', 'hunger', 'weary'
                ):
            # так сложно потому что есть отрицательная скрытность!
            if abs(STAT.dict()[key]) < abs(value) \
                        and STAT.dict()[key]*value > 0:
                return False

        if key == 'item':
            if not await Inventory.check_item(PERS.p_id, value):
                return False

        if key == 'time':
            TIME = datetime.strptime('09:00', '%H:%M') \
                + timedelta(minutes=15*STAT.gametime)

            STRING = {
                TIME.hour in range(0, 6):    'ночь',
                TIME.hour in range(6, 9):    'утро',
                TIME.hour in range(9, 19):   'день',
                TIME.hour in range(19, 24):  'вечер',
                }.get(True, '')
            if STRING != value:
                return False
    return True
