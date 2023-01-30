from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import and_
from sqlalchemy.sql.expression import null
from base import ARHM_DB, t_events_history


class EventHistory(BaseModel):
    gametime:    int
    p_id:        int
    e_id:        int
    result:      Optional[bool] = None
    date_update: Optional[datetime] = datetime.now()

    @staticmethod
    async def get(P_ID: int) -> 'EventHistory':
        "Проверка есть ли у персонажа незаконченные ивенты"
        query = t_events_history.select(and_(
            t_events_history.c.p_id == P_ID,
            t_events_history.c.result == null()
                ))
        res = await ARHM_DB.fetch_one(query)
        if res is not None:
            return EventHistory(**res)
        else:
            raise ValueError('У персонажа не найдено событие в истории')

    @staticmethod
    async def get_list(P_ID: int) -> list:
        "Возвращает лист пройденных персонажем ивентов"
        query = t_events_history.select()\
            .with_only_columns(t_events_history.c.e_id)\
            .where(t_events_history.c.p_id == P_ID)\
            .distinct()
        res = await ARHM_DB.fetch_all(query)
        if res is not None:
            return [x['e_id'] for x in res]
        else:
            return list()

    async def new(self):
        "запись факта нового события с персонажем"
        query = t_events_history.insert().values(self.dict())
        await ARHM_DB.execute(query)

    async def write_result(self):
        "запись результата события"
        query = t_events_history.update().where(and_(
            t_events_history.c.gametime == self.gametime,
            t_events_history.c.p_id == self.p_id,
            t_events_history.c.e_id == self.e_id
                    )).values(self.dict())
        await ARHM_DB.execute(query)
