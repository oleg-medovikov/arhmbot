from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from sqlalchemy import and_
from json import loads


from base import ARHM_DB, t_shops


class Shop(BaseModel):
    s_id:          int
    l_id:          int
    stage:         int
    shop_name:     str
    demand:        str
    mess_welcome:  str
    mess_not_pass: str
    mess_goodbye:  str
    product_list:  list
    shopping_list: list
    date_update: Optional[datetime] = datetime.now()

    @staticmethod
    async def get(L_ID: int, STAGE: int) -> 'Shop':
        query = t_shops.select(and_(
                t_shops.c.l_id == L_ID,
                t_shops.c.stage == STAGE
                ))
        res = await ARHM_DB.fetch_one(query)
        if res is not None:
            return Shop(**res)
        else:
            raise ValueError('в этой локации нет магазина')

    @staticmethod
    async def get_by_id(S_ID: int) -> 'Shop':
        query = t_shops.select(
                t_shops.c.s_id == S_ID
                )
        res = await ARHM_DB.fetch_one(query)
        return Shop(**res)

    def get_demand(self):
        return loads(self.demand)

    @staticmethod
    async def get_all() -> list:
        query = t_shops.select().order_by(t_shops.c.s_id)
        list_ = []
        for row in await ARHM_DB.fetch_all(query):
            list_.append(Shop(**row).dict())

        if len(list_):
            return list_
        else:
            return [{
                's_id':           0,
                'l_id':           0,
                'stage':          1,
                'shop_name':      'ашан',
                'demand':         '{}',
                'mess_welcome':   'Добро пожаловать',
                'mess_not_pass':  'пшл прочь нищеброд',
                'mess_goodbye':   'рады видеть ещё раз',
                'product_list':   [1, 2, 4],
                'shopping_list':  [1, 2, 4],
                'date_update':    datetime.now(),
                }]

    @staticmethod
    async def update_all(list_: list) -> str:
        "Обновление всей таблицы"
        if len(list_) == 0:
            return 'Нечего обновлять'
        string = ''
        for row in list_:
            query = t_shops.select(
                t_shops.c.s_id == row['s_id']
                )
            res = await ARHM_DB.fetch_one(query)
            row['product_list'] = loads(row['product_list'])
            row['shopping_list'] = loads(row['shopping_list'])

            # если строки нет, то добавляем
            if res is None:
                string += f"добавил строку {row['shop_name']}\n"
                row['date_update'] = datetime.now()
                query = t_shops.insert().values(**row)
                await ARHM_DB.execute(query)
                continue

            # если строчка есть ищем несовпадение значений, чтобы заменить
            for key, value in dict(res).items():
                if row[key] != value and key != 'date_update':
                    string += f"обновил строку {row['shop_name']}\n"
                    row['date_update'] = datetime.now()
                    query = t_shops.update()\
                        .where(
                            t_shops.c.s_id == row['s_id'])\
                        .values(**row)
                    await ARHM_DB.execute(query)
                    break
        if string == '':
            string = 'Нечего обновлять'
        return string
