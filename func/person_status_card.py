from datetime import datetime, timedelta

from clas import Person, PersonStatus
from conf import emoji
from .weary_str import weary_str
from .hunger_str import hunger_str


def person_status_card(PERS: 'Person', STAT: 'PersonStatus') -> str:
    "генерируем краткую карточку состояния персонажа"

    DATE = datetime.fromisoformat(
            PERS.create_date
            ).strftime('%d.%m.%Y в %H:%M')
    DAYS = STAT.gametime // 96
    TIME = (
        datetime.strptime('09:00', '%H:%M')
        + timedelta(minutes=15*STAT.gametime)
        ).strftime('%H:%M')

    LIST = (
        '*Карточка персонажа*\n',
        '*ИМЯ:* ', PERS.gamename, ', ',  PERS.profession,
        '\n*Зарегистрирован', ('' if PERS.sex else 'а'), ':* ', DATE,
        '*Проведено дней в Археме:* ', DAYS,
        '\n ``` \n',
        emoji('clock'), '  ', TIME, '  ',
        emoji('dollar'), ' ',  {STAT.money}, '\n',
        emoji('heart'), ' ', STAT.health, ' из ', PERS.max_health,
        emoji('brain'), ' ', STAT.mind, ' из ', PERS.max_mind, '\n',
        emoji('strength'), ' ', STAT.strength, ' ',
        emoji('speed'), ' ', STAT.speed, ' ',
        emoji('stealth'), ' ', STAT.stealth, '\n',
        emoji('knowledge'), ' ', STAT.knowledge, ' ',
        emoji('godliness'), ' ', STAT.godliness, ' ',
        emoji('luck'), ' ', STAT.luck, '\n',
        emoji('hunger'), ' ', hunger_str(STAT.hunger), '\n',
        emoji('weary'), ' ', weary_str(STAT.weary),
        '\n ``` \n',
        '*Достижения:*',
        'нет'
        )

    MESS = ''.join(str(x) for x in LIST)

    return MESS
