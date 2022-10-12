from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Manual(BaseModel):
    m_id         : int
    m_name       : str
    order        : int
    text         : str
    date_update  : Optional[datetime] = None

