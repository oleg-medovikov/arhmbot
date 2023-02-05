from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from json import loads

from base import ARHM_DB, t_monsters


class Monster(BaseModel):
    m_id:             int
    name:             str
    description:      str
    mess_win:         str
    mess_lose_hp:     str
    mess_lose_md:     str
    check_of_stels:   int
    nigthmare:        int
    crush:            int
    phisical_resist:  int
    magic_resist:     int
    check_mind:       int
    check_fight:      int
    mind_damage:      int
    body_damage:      int
    health:           int
    price:            int
    item:             list
    experience:       int
    date_update:      Optional[datetime]

    @staticmethod
    async def get(M_ID: int) -> 'Monster':
        query = t_monsters.select(
            t_monsters.c.m_id == M_ID
            )
        res = await ARHM_DB.fetch_one(query)
        if res is not None:
            return Monster(**res)
        else:
            raise ValueError(f'Нет такого монстра! {M_ID}')

    @staticmethod
    async def update_all(list_: list) -> str:
        "Обновление всей таблицы"
        if len(list_) == 0:
            return 'Нечего обновлять'
        string = ''
        for row in list_:
            query = t_monsters.select(
                t_monsters.c.m_id == row['m_id']
                )
            res = await ARHM_DB.fetch_one(query)
            row['item'] = loads(row['item'])

            # если строки нет, то добавляем
            if res is None:
                string += f"добавил строку {row['name']}\n"
                row['date_update'] = datetime.now()
                query = t_monsters.insert().values(**row)
                await ARHM_DB.execute(query)
                continue

            # если строчка есть ищем несовпадение значений, чтобы заменить
            for key, value in dict(res).items():
                if row[key] != value and key != 'date_update':
                    string += f"обновил строку {row['name']}\n"
                    row['date_update'] = datetime.now()
                    query = t_monsters.update()\
                        .where(
                            t_monsters.c.m_id == row['m_id'])\
                        .values(**row)
                    await ARHM_DB.execute(query)
                    break
        if string == '':
            string = 'Нечего обновлять'
        return string

    @staticmethod
    async def get_all() -> list:
        query = t_monsters.select().order_by(t_monsters.c.m_id)
        list_ = []
        for row in await ARHM_DB.fetch_all(query):
            list_.append(Monster(**row).dict())
        if len(list_):
            return list_
        else:
            return [{
                'm_id':             0,
                'name':             'test',
                'description':      'test',
                'mess_win':         'test',
                'mess_lose_hp':     'test',
                'mess_lose_md':     'test',
                'check_of_stels':   0,
                'nigthmare':        0,
                'crush':            0,
                'phisical_resist':  0,
                'magic_resist':     0,
                'check_mind':       0,
                'check_fight':      0,
                'mind_damage':      0,
                'body_damage':      0,
                'health':           0,
                'price':            0,
                'item':             '[]',
                'experience':       0,
                'date_update':      datetime.now(),
                }]
