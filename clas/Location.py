from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import select
from json import loads

from base import ARHM_DB, t_karta


class Location(BaseModel):
    node_id:          int
    name_node:        str
    declension:       str
    contact_list_id:  list
    district:         str
    district_id:      int
    street:           bool
    dist:             bool
    date_update:      Optional[datetime]

    @staticmethod
    async def get(NODE_ID: int) -> 'Location':
        query = t_karta.select(
                t_karta.c.node_id == int(NODE_ID))
        res = await ARHM_DB.fetch_one(query)
        if res is not None:
            return Location(**res)
        else:
            raise ValueError('Нет такой локации!')

    @staticmethod
    async def get_districts() -> list:
        "тестовая функция"
        query = select([t_karta.c.district]).distinct()\
            .order_by(t_karta.c.district)

        res = await ARHM_DB.fetch_all(query)
        return [x[0] for x in res]

    @staticmethod
    async def nearby(NODE_ID: int):
        query = t_karta.select(
                 t_karta.c.node_id == int(NODE_ID))
        res = await ARHM_DB.fetch_one(query)

        query = t_karta.select()\
            .with_only_columns([
                t_karta.c.node_id,
                t_karta.c.name_node
                ])\
            .where(t_karta.c.node_id.in_(res['contact_list_id']))

        return await ARHM_DB.fetch_all(query)

    @staticmethod
    async def update_all(list_: list) -> str:
        "Обновление всей таблицы"
        if len(list_) == 0:
            return 'Нечего обновлять'
        string = ''
        for row in list_:
            query = t_karta.select(
                t_karta.c.node_id == row['node_id']
                )
            res = await ARHM_DB.fetch_one(query)

            row['contact_list_id'] = loads(row['contact_list_id'])

            # если строки нет, то добавляем
            if res is None:
                string += f"добавил строку {row['name_node']}\n"
                row['date_update'] = datetime.now()
                query = t_karta.insert().values(**row)
                await ARHM_DB.execute(query)
                continue

            # если строчка есть ищем несовпадение значений, чтобы заменить
            for key, value in dict(res).items():
                if row[key] != value and key != 'date_update':
                    string += f"обновил строку {row['name_node']}\n"
                    row['date_update'] = datetime.now()
                    query = t_karta.update()\
                        .where(
                            t_karta.c.node_id == row['node_id'])\
                        .values(**row)
                    await ARHM_DB.execute(query)
                    break
        if string == '':
            string = 'Нечего обновлять'
        return string

    @staticmethod
    async def get_all() -> list:
        query = t_karta.select().order_by(t_karta.c.node_id)
        list_ = []
        for row in await ARHM_DB.fetch_all(query):
            list_.append(Location(**row).dict())

        if len(list_):
            return list_
        else:
            return [{
                'node_id':         0,
                'name_node':       'test',
                'declension':      'testа',
                'contact_list_id': '[0]',
                'district':        'test',
                'district_id':      0,
                'street':           True,
                'dist':             True,
                'date_update':      datetime.now(),
                }]


