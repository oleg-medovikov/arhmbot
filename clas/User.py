from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from base import ARHM_DB, t_users


class User(BaseModel):
    u_id:        int
    tg_id:       int
    username:    str
    name_tg:     str
    admin:       bool
    date_create: datetime

    @staticmethod
    async def get(TG_ID: int) -> Optional['User']:
        "Берем пользователя по телеграм id"
        query = t_users.select(t_users.c.tg_id == TG_ID)
        res = await ARHM_DB.fetch_one(query)
        if res is not None:
            return User(**res)

    @staticmethod
    async def get_all() -> list:
        "выгружаем из базы всех пользователей"
        query = t_users.select().order_by(t_users.c.u_id)
        list_ = []
        for row in await ARHM_DB.fetch_all(query):
            list_.append(User(**row).dict())
        return list_

    @staticmethod
    async def create(TG_ID: int, USERNAME: str, NAME_TG: str) -> 'User':
        "создаём нового пользователя"
        query = t_users.select(t_users.c.tg_id == TG_ID)
        res = await ARHM_DB.fetch_one(query)
        if res is not None:
            return User(**res)
        values = {
            'tg_id':       TG_ID,
            'username':    USERNAME,
            'name_tg':     NAME_TG,
            'admin':       False,
            'date_create': datetime.now(),
            }
        query = t_users.insert().values(**values)
        await ARHM_DB.execute(query)

        query = t_users.select(t_users.c.tg_id == TG_ID)
        res = await ARHM_DB.fetch_one(query)
        return User(**res)
