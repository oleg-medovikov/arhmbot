from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import and_, desc

from base import ARHM_DB, t_journal


class Journal(BaseModel):
    gametime:    int
    p_id:        int
    name:        str
    metka:       int
    mess:        str
    date_create: Optional[datetime]

    async def add(self):
        self.date_create = datetime.now()
        query = t_journal.insert().values(
            self.dict()
        )

        await ARHM_DB.execute(query)

    @staticmethod
    async def get_relocations(P_ID: int, START: int, STOP: int) -> list:
        "возвращаем последние посещенные локации"
        query = t_journal.select().where(and_(
            t_journal.c.p_id == P_ID,
            t_journal.c.metka.between(10000, 19999)
        )).order_by(desc(t_journal.c.gametime))

        list_ = []

        for key, row in enumerate(await ARHM_DB.fetch_all(query)):
            if key < START:
                continue
            if key > STOP:
                break

            list_.append(Journal(**row))

        return list_

    @staticmethod
    async def get_relocation(P_ID: int, MICRO: int) -> 'Journal':
        query = t_journal.select().where(and_(
            t_journal.c.p_id == P_ID,
            t_journal.c.date_create.microseconds == MICRO
        ))
        res = await ARHM_DB.fetch_one(query)
        return Journal(**res)

    @staticmethod
    async def get_relocation_map(P_ID: int) -> list:
        query = t_journal.select().where(and_(
            t_journal.c.p_id == P_ID,
            t_journal.c.metka.between(10000, 19999)
        )).distinct()

        list_ = []
        for row in await ARHM_DB.fetch_all(query):
            a = int(str(row['metka'])[1:3])
            b = int(str(row['metka'])[3:6])
            list_.append([a, b])
        return list_
