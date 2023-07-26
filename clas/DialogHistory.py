from pydantic import BaseModel
from sqlalchemy import and_
from sqlalchemy.sql.expression import false

from base import ARHM_DB, t_dialogs_history


class DialogHistory(BaseModel):
    p_id:     int
    s_id:     int
    d_id:     int
    q_id:     int
    result:   bool

    @staticmethod
    async def check(P_ID: int) -> 'DialogHistory':
        query = t_dialogs_history.select().where(and_(
            t_dialogs_history.c.result is false,
            t_dialogs_history.c.p_id == P_ID
        ))

        res = await ARHM_DB.fetch_one(query)
        if res is None:
            raise ValueError('нет незаконченных диалогов')
        else:
            return DialogHistory(**res)

    @staticmethod
    async def get(P_ID: int) -> 'DialogHistory':
        query = t_dialogs_history.select(
            t_dialogs_history.c.p_id == P_ID
        )
        return DialogHistory(**ARHM_DB.fetch_one(query))

    async def add(self) -> None:
        query = t_dialogs_history.select(
            t_dialogs_history.c.p_id == self.p_id
        )
        res = await ARHM_DB.fetch_one(query)
        if res is None:
            query = t_dialogs_history.insert().values(
                **self.dict()
            )
        else:
            query = t_dialogs_history.update().values(
                **self.dict()
            )
        await ARHM_DB.execute(query)

    async def update(self) -> None:
        query = t_dialogs_history.update().where(
            t_dialogs_history.c.p_id == self.p_id
        ).values(
            **self.dict()
        )
        ARHM_DB.execute(query)
