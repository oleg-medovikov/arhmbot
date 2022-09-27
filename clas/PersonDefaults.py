from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PersonDefaults(BaseModel):
    date_update        : Optional[datetime] = None
    profession         : str
    start_location_id  : int
    money_min          : int
    money_max          : int
    start_list_items   : Optional[str] = '[]'
    max_health_min     : int
    max_health_max     : int
    max_mind_min       : int
    max_mind_max       : int
    speed_min          : int
    speed_max          : int
    stealth_min        : int
    stealth_max        : int
    strength_min       : int
    strength_max       : int
    knowledge_min      : int
    knowledge_max      : int
    godliness_min      : int
    godliness_max      : int
    luck_min           : int
    luck_max           : int
