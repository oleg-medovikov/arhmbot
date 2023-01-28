from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import and_

from base import ARHM_DB, t_drop_items


class DropItem(BaseModel):
    di_id:    Optional[int]
    node_id:  int
    i_id:     int
    stage:    int
    gamename: str
    comment:  str
    time:     Optional[datetime] = datetime.now()

    async def new(self):
        "добавление нового выпавшего предмета"
        values = self.dict()
        values.pop('di_id')
        query = t_drop_items.insert().values(**values)

        await ARHM_DB.execute(query)

    @staticmethod
    async def get_by_id(DI_ID: int) -> 'DropItem':
        query = t_drop_items.select().where(
            t_drop_items.c.di_id == DI_ID
                )
        res = await ARHM_DB.fetch_one(query)
        if res is not None:
            return DropItem(**res)
        else:
            raise ValueError('Кто-то поднял предмет раньше')

    @staticmethod
    async def get(NODE_ID: int, STAGE: int) -> 'DropItem':
        query = t_drop_items.select().where(and_(
            t_drop_items.c.node_id == NODE_ID,
            t_drop_items.c.stage == STAGE))
        res = await ARHM_DB.fetch_one(query)
        if res is not None:
            return DropItem(**res)
        else:
            raise ValueError('На локации нет потерянных предметов')

    async def delete_from_location(self):
        query = t_drop_items.delete().where(
            t_drop_items.c.di_id == self.di_id
            )
        await ARHM_DB.execute(query)
