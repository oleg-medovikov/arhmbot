from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import and_
from json import loads
from asyncpg.exceptions import DataError
from json.decoder import JSONDecodeError

from base import ARHM_DB, t_dialogs


class Dialog(BaseModel):
    d_id:         int
    q_id:         int
    name:         str
    description:  str
    answers:      list
    transfer:     list
    demaind:      str
    buy_items:    list
    buy_costs:    list
    sale_items:   list
    sale_costs:   list
    date_update:  datetime

    @staticmethod
    async def get(D_ID: int, Q_ID: int) -> 'Dialog':
        query = t_dialogs.select(and_(
                t_dialogs.c.d_id == D_ID,
                t_dialogs.c.q_id == Q_ID
                ))
        res = await ARHM_DB.fetch_one(query)
        if res is not None:
            return Dialog(**res)
        else:
            raise ValueError(f'Нет такого диалога {D_ID} {Q_ID}')

    @staticmethod
    async def get_dialog(D_ID: int) -> list:
        query = t_dialogs.select().where(
            t_dialogs.c.d_id == D_ID
        )
        res = await ARHM_DB.fetch_all(query)
        return [dict(_) for _ in res]

    @staticmethod
    async def get_all() -> list:
        query = t_dialogs.select().order_by(
            t_dialogs.c.d_id,
            t_dialogs.c.q_id
                )
        list_ = []
        for row in await ARHM_DB.fetch_all(query):
            list_.append(Dialog(**row).dict())

        if len(list_):
            return list_
        else:
            return [{
                'd_id':         0,
                'q_id':         0,
                'name':        'Название диалога',
                'description': 'Описание ситуции',
                'answers':     '[]',
                'transfer':    '[]',
                'demaind':     '{}',
                'buy_items':   '[]',
                'buy_costs':   '[]',
                'sale_items':  '[]',
                'sale_costs':  '[]',
                'date_update':  datetime.now(),
                }]

    @staticmethod
    async def update_all(list_: list) -> str:
        "Обновление всей таблицы"
        if len(list_) == 0:
            return 'Нечего обновлять'
        string = ''
        for row in list_:
            query = t_dialogs.select(and_(
                t_dialogs.c.d_id == row['d_id'],
                t_dialogs.c.q_id == row['q_id']
                ))
            res = await ARHM_DB.fetch_one(query)
            try:
                row['answers'] = loads(row['answers'])
                row['transfer'] = loads(row['transfer'])
                row['buy_items'] = loads(row['buy_items'])
                row['buy_costs'] = loads(row['buy_costs'])
                row['sale_items'] = loads(row['sale_items'])
                row['sale_costs'] = loads(row['sale_costs'])
            except JSONDecodeError:
                string += f"ошибка {row['name']} {row['q_id']}\n"
                continue

            # если строки нет, то добавляем
            if res is None:
                string += f"добавил строку {row['name']} {row['q_id']}\n"
                row['date_update'] = datetime.now()
                query = t_dialogs.insert().values(**row)
                await ARHM_DB.execute(query)
                continue

            # если строчка есть ищем несовпадение значений, чтобы заменить
            for key, value in dict(res).items():
                if row[key] != value and key != 'date_update':
                    string += f"обновил строку {row['name']} {row['q_id']}\n"
                    row['date_update'] = datetime.now()
                    query = t_dialogs.update()\
                        .where(and_(
                            t_dialogs.c.d_id == row['d_id'],
                            t_dialogs.c.q_id == row['q_id']
                                ))\
                        .values(**row)
                    try:
                        await ARHM_DB.execute(query)
                    except DataError:
                        string += f"ошибка в строке {row['name']} {row['q_id']}\n"

                    break
        if string == '':
            string = 'Нечего обновлять'
        return string
