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
        j = t_users.join(
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
                    )).select_from(j)

        res = await ARHM_DB.fetch_one(query)

        return Person(**res), PersonStatus(**res)

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

    async def change(self, KEY: str, VALUE: int) -> 'PersonStatus':
        "изменение 1 параметра в базе"
        DICT = {}
        OLD = self.dict().get(KEY)

        L_STANDART = [
            'speed', 'stealth', 'strength', 'knowledge',
            'godliness', 'luck', 'experience', 'bless', 'proof',
            'money', 'health', 'mind'
            ]
        L_POSITIVE = ['hunger', 'weary']
        L_ID = ['location']
        L_BOOL = ['death']

        DICT[KEY] = {
            KEY in L_STANDART:   OLD + VALUE,
            KEY in L_POSITIVE:   OLD + VALUE if OLD + VALUE > 0 else 0,
            KEY in L_ID:         VALUE,
            KEY in L_BOOL:       bool(VALUE),
            }.get(True, OLD)

        DICT['date_update'] = datetime.now()

        query = t_persons_status.update().where(
            t_persons_status.c.p_id == self.p_id
                ).values(**DICT)

        await ARHM_DB.execute(query)
        # вытаскиваем измененную строку
        query = t_persons_status.select(
            t_persons_status.c.p_id == self.p_id
                )
        res = await ARHM_DB.fetch_one(query)
        return PersonStatus(**res)

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

    async def waste_time(self, TIME: int):
        "Тратим игровое время в зависимости от скорости персонажа"
        if self.speed > 10:
            TOTAL = 1
        else:
            TOTAL = TIME * (6 - self.speed//2)

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

    async def dice_roll(self, COUNT: int) -> dict:
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
