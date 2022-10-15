from datetime import datetime
from pydantic import BaseModel
from typing   import Optional


class Item(BaseModel):
    i_id          : int
    name          : str
    description   : str
    equip_mess    : str
    fail_mess     : str
    remove_mess   : str
    drop_mess     : str
    i_type        : str
    slot          : str
    effect        : str
    demand        : str
    emoji         : str
    cost          : int
    single_use    : bool
    achievement   : bool
    date_update   : Optional[datetime] = None
