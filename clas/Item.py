from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import json

from base import ARHM_DB, t_items


class Item(BaseModel):
    i_id:           int
    name:           str
    description:    str
    equip_mess:     str
    fail_mess:      str
    remove_mess:    str
    drop_mess:      str
    i_type:         str
    slot:           str
    effect:         str
    demand:         str
    emoji:          str
    cost:           int
    single_use:     bool
    achievement:    bool
    date_update:    Optional[datetime] = None

    @staticmethod
    async def get(I_ID: int) -> 'Item':
        query = t_items.select(
            t_items.c.i_id == int(I_ID)
            )
        res = await ARHM_DB.fetch_one(query)
        if res is not None:
            return Item(**res)
        else:
            raise ValueError(f'Нет такого предмета! {I_ID}')

    @staticmethod
    async def get_all():
        query = t_items.select().order_by(t_items.c.i_id)
        list_ = []
        for row in await ARHM_DB.fetch_all(query):
            list_.append(Item(**row).dict())
        if len(list_):
            return list_
        else:
            return [{
                'i_id':         0,
                'name':         'test',
                'description':  'test',
                'equip_mess':   'test',
                'fail_mess':    'test',
                'remove_mess':  'test',
                'drop_mess':    'test',
                'i_type':       'test',
                'slot':         'onehand',
                'effect':       '[]',
                'demand':       '[]',
                'emoji':        'test',
                'cost':         0,
                'single_use':   True,
                'achievement':  False,
                'date_update':  datetime.now(),
                }]

    @staticmethod
    async def update_all(list_: list) -> str:
        "Обновление всей таблицы"
        if len(list_) == 0:
            return 'Нечего обновлять'
        string = ''
        for row in list_:
            query = t_items.select(
                t_items.c.i_id == row['i_id']
                )
            res = await ARHM_DB.fetch_one(query)

            # если строки нет, то добавляем
            if res is None:
                string += f"добавил строку {row['name']}\n"
                row['date_update'] = datetime.now()
                query = t_items.insert().values(**row)
                await ARHM_DB.execute(query)
                continue

            # если строчка есть ищем несовпадение значений, чтобы заменить
            for key, value in dict(res).items():
                if row[key] != value and key != 'date_update':
                    string += f"обновил строку {row['name']}\n"
                    row['date_update'] = datetime.now()
                    query = t_items.update()\
                        .where(
                            t_items.c.i_id == row['i_id'])\
                        .values(**row)
                    await ARHM_DB.execute(query)
        if string == '':
            string = 'Нечего обновлять'
        return string
