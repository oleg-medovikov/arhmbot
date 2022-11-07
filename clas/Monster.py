from datetime import datetime
from pydantic import BaseModel
from typing   import Optional

class Monster(BaseModel):
    m_id            : int
    name            : str
    description     : str
    mess_win        : str
    mess_lose       : str
    check_of_stels  : int
    nigthmare       : int
    crush           : int
    phisical_resist : int
    magic_resist    : int
    check_mind      : int
    check_fight     : int
    mind_damage     : int
    body_damage     : int
    health          : int
    price           : int
    item            : str
    experience      : int
    date_update     : Optional[datetime] = None
