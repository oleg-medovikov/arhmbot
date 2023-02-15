from datetime import datetime, timedelta

from clas import Person, PersonStatus, Inventory


async def check_pers(pers, key, value) -> bool:
    return pers.dict()[key] == value


async def check_location(stat, value) -> bool:
    return stat == value


async def less_money(stat: int, value: int) -> bool:
    "проверка что денег мало, меньше, чем значение"
    return stat < value


async def time_cheack(gametime: int, VALUE: str) -> bool:
    TIME = datetime.strptime('09:00', '%H:%M') \
        + timedelta(minutes=15*gametime)

    STRING = {
        TIME.hour in range(0,  6):  'ночь',
        TIME.hour in range(6,  9):  'утро',
        TIME.hour in range(9,  19): 'день',
        TIME.hour in range(19, 24): 'вечер',
        }.get(True, '')
    return STRING == VALUE


async def check_stat(stat, key: str, value: int) -> bool:
    "числовые проверки"
    INT = stat.dict()[key]
    return abs(INT) > abs(value) and INT*value > 0


LIST_STAT = [
    'money', 'health', 'mind', 'speed',
    'stealth', 'strength', 'knowledge',
    'godliness', 'luck', 'hunger', 'weary'
        ]

LIST_PERS = [
        'sex', 'profession'
        ]


async def demand(PERS: 'Person', STAT: 'PersonStatus', DEMAND: dict) -> bool:
    "Прохождение проверки персонажем"
    INVE = await Inventory.get(PERS)
    for key, value in DEMAND.items():
        CHECK = {
            key in LIST_PERS:    check_pers(PERS, key, value),
            key == 'location':   check_location(STAT.location, value),
            key in LIST_STAT:    check_stat(STAT, key, value),
            key == 'time':       time_cheack(STAT.gametime, value),
            key == 'less_money': less_money(STAT.money, value),
            key == 'item':       INVE.check_item(value),
            key == 'not_item':   INVE.check_not_item(value),
                }.get(True, True)

        if not await CHECK:
            return False
    return True
