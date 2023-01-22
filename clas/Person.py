from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import and_
from random import randint

from base import ARHM_DB, t_persons
from .PersonDefaults import PersonDefaults


class Person(BaseModel):
    p_id:               int
    u_id:               int
    gamename:           str
    create_date:        datetime
    sex:                bool
    profession:         str
    destination:        str
    start_location_id:  int
    start_money:        int
    max_health:         int
    max_mind:           int
    speed:              int
    stealth:            int
    strength:           int
    knowledge:          int
    godliness:          int
    luck:               int
    death:              Optional[bool] = False
    d_reason:           Optional[str] = None
    date_death:         Optional[datetime] = None

    @staticmethod
    async def create(
        U_ID:         int,
        GAMENAME:     str,
        SEX:          bool,
        PROFESSION:   str,
        DESTINATION:  str
            ) -> 'Person':
        "вытаскиваем живого персонажа, если он есть"
        query = t_persons.select(and_(
           t_persons.c.u_id == U_ID,
           t_persons.c.death is False))
        res = await ARHM_DB.fetch_one(query)
        if res is not None:
            return Person(**res)

        # вытаскиваем дефолтные значения для профессии
        DEF = await PersonDefaults.get(PROFESSION)
        # Генерим случайные значения
        values = {
            'u_id':          U_ID,
            'gamename':      GAMENAME,
            'create_date':   datetime.now(),
            'sex':           SEX,
            'profession':    PROFESSION,
            'destination':   DESTINATION,
            'death':         False,
            'start_location_id':  DEF.start_location_id,
            'start_money':   randint(DEF.money_min,      DEF.money_max),
            'max_health':    randint(DEF.max_health_min, DEF.max_health_max),
            'max_mind':      randint(DEF.max_mind_min,   DEF.max_mind_max),
            'speed':         randint(DEF.speed_min,      DEF.speed_max),
            'stealth':       randint(DEF.stealth_min,    DEF.stealth_max),
            'strength':      randint(DEF.strength_min,   DEF.strength_max),
            'knowledge':     randint(DEF.knowledge_min,  DEF.knowledge_max),
            'godliness':     randint(DEF.godliness_min,  DEF.godliness_max),
            'luck':          randint(DEF.luck_min,       DEF.luck_max)
           }

        query = t_persons.insert().values(**values)
        await ARHM_DB.execute(query)
        # вытаскиваем созданного персонажа
        query = t_persons.select(and_(
           t_persons.c.u_id == U_ID,
           t_persons.c.death is False))
        res = await ARHM_DB.fetch_one(query)
        return Person(**res)

    @staticmethod
    async def cheak(U_ID: int) -> bool:
        """"Проверка наличия живого персонажа"""
        quary = t_persons.select(and_(
            t_persons.c.u_id == U_ID,
            t_persons.c.death is False
            ))
        res = await ARHM_DB.fetch_one(quary)
        return res is not None

    @staticmethod
    async def get(U_ID: int) -> Optional['Person']:
        """
        вытаскиваем живого персонажа пользователя
        или ничего, если такого нет
        """
        quary = t_persons.select(and_(
            t_persons.c.u_id == U_ID,
            t_persons.c.death is False
            ))
        res = await ARHM_DB.fetch_one(quary)
        if res is not None:
            return Person(**res)

    async def die(self, REASON):
        "персонаж умирает"
        query = t_persons.update()\
            .where(t_persons.c.p_id == self.p_id)\
            .values(
                death=True,
                d_reason=REASON,
                date_death=datetime.now()
                )
        await ARHM_DB.execute(query)
