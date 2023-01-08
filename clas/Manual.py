from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from base import ARHM_DB, t_manual


class Manual(BaseModel):
    m_id:        int
    m_name:      str
    order:       int
    text:        str
    date_update: Optional[datetime] = datetime.now()

    @staticmethod
    async def get(M_ID: int) -> str:
        query = t_manual.select(
                t_manual.c.m_id == int(M_ID))
        res = await ARHM_DB.fetch_one(query)
        try:
            return res['text']
        except ValueError:
            return f'Нет такой строчки мануала {M_ID}'

    @staticmethod
    async def get_all() -> list:
        query = t_manual.select().order_by(t_manual.c.order)
        list_ = []
        for row in await ARHM_DB.fetch_all(query):
            list_.append(Manual(**row).dict())

        if len(list_):
            return list_
        else:
            return [{
                'm_id':         '0',
                'm_name':       'Название кнопочки',
                'order':        '0',
                'text':         'какой-то текст, поясняющий тему кнопки',
                'date_update':  datetime.now(),
                }]

    @staticmethod
    async def update_all(list_: list) -> str:
        "Обновление всей таблицы"
        if len(list_) == 0:
            return 'Нечего обновлять'
        string = ''
        for row in list_:
            query = t_manual.select(
                t_manual.c.m_id == row['m_id']
                )
            res = await ARHM_DB.fetch_one(query)

            # если строки нет, то добавляем
            if res is None:
                string += f"добавил строку {row['m_name']}\n"
                row['date_update'] = datetime.now()
                query = t_manual.insert().values(**row)
                await ARHM_DB.execute(query)
                continue

            # если строчка есть ищем несовпадение значений, чтобы заменить
            for key, value in dict(res).items():
                if row[key] != value and key != 'date_update':
                    string += f"обновил строку {row['m_name']}\n"
                    row['date_update'] = datetime.now()
                    query = t_manual.update()\
                        .where(
                            t_manual.c.m_id == row['m_id'])\
                        .values(**row)
                    await ARHM_DB.execute(query)
        if string == '':
            string = 'Нечего обновлять'
        return string
