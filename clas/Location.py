from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Location(BaseModel):
    node_id         : int
    name_node       : str
    declension      : str
    contact_list_id : str
    district        : str
    district_id     : int
    street          : bool
    dist            : bool
    date_update     : Optional[datetime] = None

