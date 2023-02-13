from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from random import randint
from sqlalchemy import and_, select
from sqlalchemy.sql.expression import false

from base import ARHM_DB, t_users, t_persons_status, t_persons
from .Person import Person

from conf import MAX_HUNGER, MAX_WEARY


class PersonStatus(BaseModel):
    date_update:  Optional[datetime] = None
    p_id:         int
    death:        Optional[bool] = False
    gametime:     int
    stage:        int
    money:        int
    location:     int
    health:       int
    mind:         int
    speed:        int
    stealth:      int
    strength:     int
    knowledge:    int
    godliness:    int
    luck:         int
    experience:   int
    bless:        int
    proof:        int
    hunger:       int
    weary:        int

    @staticmethod
    async def get_all(T_ID: int) -> tuple['Person', 'PersonStatus']:
        """Возвращаем сразу 2 объекта, чтобы было меньше sql запросов"""
        join = t_users.join(
            t_persons,
            t_persons.c.u_id == t_users.c.u_id
                ).join(
                t_persons_status,
                t_persons_status.c.p_id == t_persons.c.p_id
                    )

        query = select(
                *t_persons.columns,
                *t_persons_status.columns
                ).where(and_(
                    t_users.c.tg_id == T_ID,
                    t_persons.c.death == false()
                    )).select_from(join)

        res = await ARHM_DB.fetch_one(query)
        pers_val = {
            'p_id':              res['p_id'],
            'u_id':              res['u_id'],
            'gamename':          res['gamename'],
            'create_date':       res['create_date'],
            'sex':               res['sex'],
            'profession':        res['profession'],
            'destination':       res['destination'],
            'start_location_id': res['start_location_id'],
            'start_money':       res['start_money'],
            'max_health':        res['max_health'],
            'max_mind':          res['max_mind'],
            'speed':             res['speed'],
            'stealth':           res['stealth'],
            'strength':          res['strength'],
            'knowledge':         res['knowledge'],
            'godliness':         res['godliness'],
            'luck':              res['luck'],
            'death':             res['death'],
            'd_reason':          res['d_reason'],
            'date_death':        res['date_death'],
                }
        stat_val = {
            'p_id':        res['p_id'],
            'death':       res['death_1'],
            'gametime':    res['gametime'],
            'stage':       res['stage'],
            'money':       res['money'],
            'location':    res['location'],
            'health':      res['health'],
            'mind':        res['mind'],
            'speed':       res['speed_1'],
            'stealth':     res['stealth_1'],
            'strength':    res['strength_1'],
            'knowledge':   res['knowledge_1'],
            'godliness':   res['godliness_1'],
            'luck':        res['luck_1'],
            'experience':  res['experience'],
            'bless':       res['bless'],
            'proof':       res['proof'],
            'hunger':      res['hunger'],
            'weary':       res['weary'],
            'date_update': res['date_update'],
                }

        return Person(**pers_val), PersonStatus(**stat_val)

    @staticmethod
    async def get(PERSON: 'Person') -> 'PersonStatus':
        # достаем статус персонажа по p_id
        query = t_persons_status.select(
            t_persons_status.c.p_id == PERSON.p_id
                )
        res = await ARHM_DB.fetch_one(query)

        if res is not None:
            return PersonStatus(**res)
        else:
            # генерируем новый статус, если нет старого
            values = {
                'date_update': datetime.now(),
                'p_id':        PERSON.p_id,
                'death':       False,
                'gametime':    1,
                'stage':       1,
                'money':       PERSON.start_money,
                'location':    PERSON.start_location_id,
                'health':      PERSON.max_health,
                'mind':        PERSON.max_mind,
                'speed':       PERSON.speed,
                'stealth':     PERSON.stealth,
                'strength':    PERSON.strength,
                'knowledge':   PERSON.knowledge,
                'godliness':   PERSON.godliness,
                'luck':        PERSON.luck,
                'experience':  0,
                'bless':       0,
                'proof':       0,
                'hunger':      0,
                'weary':       0,
                }

            query = t_persons_status.insert().values(**values)
            await ARHM_DB.execute(query)
            return PersonStatus(**values)

    async def change(self, KEY: str, VALUE: int):
        "изменение 1 параметра в базе"

        L_STANDART = [
            'speed', 'stealth', 'strength', 'knowledge',
            'godliness', 'luck', 'experience', 'bless', 'proof',
            'money', 'health', 'mind'
            ]
        L_POSITIVE = ['hunger', 'weary']
        L_ID = ['location']
        L_BOOL = ['death']

        OLD = getattr(self, KEY)
        ITOG = {
            KEY in L_STANDART:   OLD + VALUE,
            KEY in L_POSITIVE:   OLD + VALUE if OLD + VALUE > 0 else 0,
            KEY in L_ID:         VALUE,
            KEY in L_BOOL:       bool(VALUE),
            }.get(True, OLD)

        setattr(self, KEY, ITOG)

        query = t_persons_status.update().where(
            t_persons_status.c.p_id == self.p_id
            ).values(**{KEY: ITOG, 'date_update': datetime.now()})

        await ARHM_DB.execute(query)

    async def update(self):
        "синхронизируем объект класса с базой данных"
        query = t_persons_status.select(
            t_persons_status.c.p_id == self.p_id
                )
        res = await ARHM_DB.fetch_one(query)

        self.date_update = datetime.now()

        if res is None:
            query = t_persons_status.insert().values(self.dict())
            await ARHM_DB.execute(query)
        else:
            query = t_persons_status.update()\
                .where(t_persons_status.c.p_id == self.p_id)\
                .values(**self.dict())
            await ARHM_DB.execute(query)

    async def waste_time(self, TIME: int) -> int:
        "Тратим игровое время в зависимости от скорости персонажа"
        if TIME < 1:
            return 0

        TOTAL = {
            self.speed > 9:      1,
            self.speed < 1:       TIME*6,
            0 < self.speed < 10:  TIME * (6 - self.speed//2),
                }[True]

        self.gametime += TOTAL
        self.hunger += TOTAL
        self.weary += TOTAL

        # если слишком голодный или усталый, то снижаем показатели
        if self.hunger > MAX_HUNGER:
            delta = (self.hunger - MAX_HUNGER) // 4
            if delta > 0:
                self.health -= delta
                self.hunger = MAX_HUNGER

        if self.weary > MAX_WEARY:
            delta = (self.weary - MAX_WEARY) // 4
            if delta > 0:
                self.mind -= delta
                self.weary = MAX_WEARY

        query = t_persons_status.update()\
            .where(t_persons_status.c.p_id == self.p_id)\
            .values(**self.dict())
        await ARHM_DB.execute(query)

        return TOTAL

    def dice_roll(self, COUNT: int) -> dict:
        "кидаем кубик и считаем количество успешных проверок"

        # 5% шанс дополнительного броска за каждую удачу
        LUCK = sum(randint(0, 100) // 95 for _ in range(self.luck))
        # кидаем кубики
        NUMBERS = [randint(1, 6) for _ in range(COUNT + LUCK)]
        # проверяем благословение
        CHECK_LIST = {
            self.bless == 0:  [5, 6],
            self.bless > 0:   [4, 5, 6],
            self.bless < 0:   [6],
            }[True]
        # считаем количество успешных проверок
        CHECK_PASSED = sum([NUMBERS.count(x) for x in CHECK_LIST])

        return {
            'success':      bool(CHECK_PASSED),
            'luck':         LUCK,
            'numbers':      NUMBERS,
            'check_passed': CHECK_PASSED
                }
