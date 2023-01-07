from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import and_, select

from base import ARHM_DB, t_karta_descriptions, t_karta


class LocationDescription(BaseModel):
    node_id:      int
    stage:        int
    description:  str
    date_update:  Optional[datetime]

    @staticmethod
    async def get(NODE_ID: int, STAGE: int) -> str:
        query = t_karta_descriptions.select(and_(
                t_karta_descriptions.c.node_id == NODE_ID,
                t_karta_descriptions.c.stage == STAGE
                ))
        res = await ARHM_DB.fetch_one(query)
        try:
            return res['description']
        except KeyError:
            return "какая жаль, для этой локации не написано описание!"

    @staticmethod
    async def get_all():
        j = t_karta_descriptions.join(
                t_karta,
                t_karta_descriptions.c.node_id == t_karta.c.node_id
                )
        query = select([
                t_karta_descriptions.c.node_id,
                t_karta_descriptions.c.stage,
                t_karta.c.name_node,
                t_karta_descriptions.c.description,
                t_karta_descriptions.c.date_update
                ]).order_by(t_karta_descriptions.c.node_id).select_from(j)

        list_ = []
        for row in await ARHM_DB.fetch_all(query):
            list_.append(LocationDescription(**row).dict())
        if len(list_):
            return list_
        else:
            return [{
                'node_id':    '0',
                'stage':      '0',
                'description': 'какое-то описание',
                'date_update': datetime.now()
                }]

    @staticmethod
    async def update_all(list_: list) -> str:
        "Обновление всей таблицы"
        if len(list_) == 0:
            return 'Нечего обновлять'
        string = ''
        for row in list_:
            query = t_karta_descriptions.select(and_(
                t_karta_descriptions.c.node_id == row['node_id'],
                t_karta_descriptions.c.stage == row['stage']
                ))
            res = await ARHM_DB.fetch_one(query)

            # если строки нет, то добавляем
            if res is None:
                string += f"добавил строку {row['node_id']} {row['stage']}\n"
                row['date_update'] = datetime.now()
                query = t_karta_descriptions.insert().values(**row)
                await ARHM_DB.execute(query)
                continue

            # если строчка есть ищем несовпадение значений, чтобы заменить
            for key, value in dict(res).items():
                if row[key] != value and key != 'date_update':
                    string += f"обновил строку {row['node_id']} {row['stage']}\n"
                    row['date_update'] = datetime.now()
                    query = t_karta_descriptions.update()\
                        .where(and_(
                            t_karta_descriptions.c.node_id == row['node_id'],
                            t_karta_descriptions.c.stage == row['stage']
                            ))\
                        .values(**row)
                    await ARHM_DB.execute(query)
        if string == '':
            string = 'Нечего обновлять'
        return string
