from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from base import ARHM_DB, t_persons_defaults


class PersonDefaults(BaseModel):
    profession:          str
    start_location_id:   int
    money_min:           int
    money_max:           int
    start_list_items:    str
    max_health_min:      int
    max_health_max:      int
    max_mind_min:        int
    max_mind_max:        int
    speed_min:           int
    speed_max:           int
    stealth_min:         int
    stealth_max:         int
    strength_min:        int
    strength_max:        int
    knowledge_min:       int
    knowledge_max:       int
    godliness_min:       int
    godliness_max:       int
    luck_min:            int
    luck_max:            int
    date_update:         Optional[datetime] = None

    @staticmethod
    async def get(PROFESSION: str) -> 'PersonDefaults':
        query = t_persons_defaults.select(
                t_persons_defaults.c.profession == PROFESSION)
        res = await ARHM_DB.fetch_one(query)
        if res is not None:
            return PersonDefaults(**res)
        else:
            raise ValueError('Не существует такой профессии!')

    @staticmethod
    async def update_all(list_: list) -> str:
        "Обновление всей таблицы"
        if len(list_) == 0:
            return 'Нечего обновлять'
        string = ''
        for row in list_:
            query = t_persons_defaults.select(
                t_persons_defaults.c.profession == row['profession']
                )
            res = await ARHM_DB.fetch_one(query)

            # если строки нет, то добавляем
            if res is None:
                string += f"добавил строку {row['profession']}\n"
                row['date_update'] = datetime.now()
                query = t_persons_defaults.insert().values(**row)
                await ARHM_DB.execute(query)
                continue

            # если строчка есть ищем несовпадение значений, чтобы заменить
            for key, value in dict(res).items():
                if row[key] != value and key != 'date_update':
                    string += f"обновил строку {row['profession']}\n"
                    row['date_update'] = datetime.now()
                    query = t_persons_defaults.update()\
                        .where(
                            t_persons_defaults.c.profession == row['profession'])\
                        .values(**row)
                    await ARHM_DB.execute(query)
                    break
        if string == '':
            string = 'Нечего обновлять'
        return string

    async def update(self) -> dict:
        """функция обновления строк в базе"""
        query = t_persons_defaults.select(
                t_persons_defaults.c.profession == self.profession)

        res = await ARHM_DB.fetch_one(query)
        if res is None:
            self.date_update = datetime.now()
            query = t_persons_defaults.insert().values(self.dict())
            await ARHM_DB.execute(query)
            return {'mess': f'строка {self.profession} добавлена'}
        else:
            # если строчка есть ищем несовпадение значений, чтобы заменить
            for key, value in dict(res).items():
                if self.dict()[key] != value and key != 'date_update':
                    self.date_update = datetime.now()
                    query = t_persons_defaults.update()\
                        .where(
                            t_persons_defaults.c.profession == self.profession
                            )\
                        .values(self.dict())
                    await ARHM_DB.execute(query)
                    return {'mess': f'строка {self.profession} исправлена'}
            return {'mess': f'строка {self.profession} без изменений'}

    @staticmethod
    async def get_all() -> list:
        query = t_persons_defaults.select()
        list_ = []
        for row in await ARHM_DB.fetch_all(query):
            list_.append(PersonDefaults(**row).dict())
        if len(list_):
            return list_
        return [{
            'profession':          'test',
            'start_location_id':   0,
            'money_min':           0,
            'money_max':           0,
            'start_list_items':    '[]',
            'max_health_min':      0,
            'max_health_max':      0,
            'max_mind_min':        0,
            'max_mind_max':        0,
            'speed_min':           0,
            'speed_max':           0,
            'stealth_min':         0,
            'stealth_max':         0,
            'strength_min':        0,
            'strength_max':        0,
            'knowledge_min':       0,
            'knowledge_max':       0,
            'godliness_min':       0,
            'godliness_max':       0,
            'luck_min':            0,
            'luck_max':            0,
            'date_update':         datetime.now(),
            }]
