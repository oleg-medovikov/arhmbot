from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class Event(BaseModel):
    e_id            : int
    e_name          : str
    single          : bool
    active          : bool
    stage           : int
    node_id         : int
    profession      : str
    demand          : str
    description     : str
    mess_prize      : str
    mess_punishment : str
    check           : str
    choice          : bool
    prize           : str
    punishment      : str
    username        : str
    date_update     : Optional[datetime] = None

