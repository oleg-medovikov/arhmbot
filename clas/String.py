from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from base import ARHM_DB, t_strings


class String(BaseModel):
    s_id:        int
    s_name:      str
    text:        str
    date_update: Optional[datetime] = datetime.now()

    @staticmethod
    async def get(S_ID: int) -> str:
        query = t_strings.select(
                t_strings.c.m_id == int(S_ID))
        res = await ARHM_DB.fetch_one(query)
        try:
            return res['text']
        except ValueError:
            return f'Нет такой строчки {S_ID}'

    @staticmethod
    async def get_all() -> list:
        query = t_strings.select().order_by(t_strings.c.s_id)
        list_ = []
        for row in await ARHM_DB.fetch_all(query):
            list_.append(String(**row).dict())

        if len(list_):
            return list_
        else:
            return [{
                's_id':         '0',
                's_name':       'Название строчки',
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
            query = t_strings.select(
                t_strings.c.s_id == row['s_id']
                )
            res = await ARHM_DB.fetch_one(query)

            # если строки нет, то добавляем
            if res is None:
                string += f"добавил строку {row['s_name']}\n"
                row['date_update'] = datetime.now()
                query = t_strings.insert().values(**row)
                await ARHM_DB.execute(query)
                continue

            # если строчка есть ищем несовпадение значений, чтобы заменить
            for key, value in dict(res).items():
                if row[key] != value and key != 'date_update':
                    string += f"обновил строку {row['s_name']}\n"
                    row['date_update'] = datetime.now()
                    query = t_strings.update()\
                        .where(
                            t_strings.c.s_id == row['s_id'])\
                        .values(**row)
                    await ARHM_DB.execute(query)
        if string == '':
            string = 'Нечего обновлять'
        return string
