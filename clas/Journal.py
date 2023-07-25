from datetime import datetime
from pydantic import BaseModel
from typing import Optional

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
