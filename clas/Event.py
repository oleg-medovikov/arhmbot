from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import select, and_
from sqlalchemy.sql.expression import true
import json

from base import ARHM_DB, t_events, t_karta


class Event(BaseModel):
    e_id:             int
    e_name:           str
    single:           bool
    active:           bool
    stage:            int
    node_id:          int
    profession:       str
    demand:           str
    description:      str
    mess_prize:       str
    mess_punishment:  str
    check:            str
    choice:           bool
    prize:            str
    punishment:       str
    username:         str
    date_update:      Optional[datetime]

    @staticmethod
    async def location(NODE_ID: int, STAGE: int, PROFESSION: str) -> list:
        "вытащить все активные события для данной локации"
        query = t_events.select(and_(
                t_events.c.active == true(),
                t_events.c.node_id == NODE_ID,
                t_events.c.stage == STAGE,
                t_events.c.profession.in_((PROFESSION, 'все')),
                ))
        list_ = []
        for row in await ARHM_DB.fetch_all(query):
            list_.append(Event(**row))
        return list_

    @staticmethod
    async def get(E_ID: int) -> 'Event':
        query = t_events.select(
            t_events.c.e_id == E_ID
                )
        res = await ARHM_DB.fetch_one(query)
        if res is not None:
            return Event(**res)
        else:
            raise ValueError(f'Нет такого события! {E_ID}')

    def get_choice(self) -> list:
        if self.choice:
            return json.loads(self.check)['choice']
        else:
            return []

    def get_check(self) -> dict:
        "choice тут не нужен!"
        d = json.loads(self.check)
        try:
            del d['choice']
        except KeyError:
            pass
        return d

    def get_monster(self) -> int:
        d = json.loads(self.check)
        return d['monster']

    def get_demand(self) -> dict:
        return json.loads(self.demand)

    def get_prize(self) -> dict:
        return json.loads(self.prize)

    def get_punishment(self) -> dict:
        return json.loads(self.punishment)

    @staticmethod
    async def get_all() -> list:
        j = t_events.join(
                t_karta,
                t_events.c.node_id == t_karta.c.node_id
                )
        query = select([
            t_events.c.e_id,
            t_events.c.e_name,
            t_events.c.single,
            t_events.c.active,
            t_events.c.stage,
            t_events.c.node_id,
            t_karta.c.name_node,
            t_karta.c.district,
            t_events.c.profession,
            t_events.c.demand,
            t_events.c.description,
            t_events.c.mess_prize,
            t_events.c.mess_punishment,
            t_events.c.check,
            t_events.c.choice,
            t_events.c.prize,
            t_events.c.punishment,
            t_events.c.username,
            t_events.c.date_update,
            ]).order_by(t_events.c.e_id).select_from(j)
        list_ = []
        for row in await ARHM_DB.fetch_all(query):
            list_.append(Event(**row).dict())
        if len(list_):
            return list_
        else:
            return [{
                'e_id':             0,
                'e_name':           'test',
                'single':           True,
                'active':           True,
                'stage':            1,
                'node_id':          0,
                'name_node':        'test',
                'district':         'test',
                'profession':       'test',
                'demand':           '{}',
                'description':      'test',
                'mess_prize':       'test',
                'mess_punishment':  'test',
                'check':            '{}',
                'choice':           False,
                'prize':            '{}',
                'punishment':       '{}',
                'username':         'test',
                'date_update':      datetime.now()
                }]

    @staticmethod
    async def update_all(list_: list) -> str:
        "Обновление всей таблицы"
        if len(list_) == 0:
            return 'Нечего обновлять'
        string = ''
        for row in list_:
            query = t_events.select(
                t_events.c.e_id == row['e_id']
                )
            res = await ARHM_DB.fetch_one(query)

            # если строки нет, то добавляем
            if res is None:
                string += f"добавил строку {row['e_name']}\n"
                row['date_update'] = datetime.now()
                query = t_events.insert().values(**row)
                await ARHM_DB.execute(query)
                continue

            # если строчка есть ищем несовпадение значений, чтобы заменить
            for key, value in dict(res).items():
                if row[key] != value and key != 'date_update':
                    string += f"обновил строку {row['e_name']}\n"
                    row['date_update'] = datetime.now()
                    query = t_events.update()\
                        .where(
                            t_events.c.e_id == row['e_id'])\
                        .values(**row)
                    await ARHM_DB.execute(query)
                    break
        if string == '':
            string = 'Нечего обновлять'
        return string
