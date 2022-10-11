from datetime import datetime
from pydantic import BaseModel
from typing   import Optional
 
class LocationDescription(BaseModel):
    node_id     : int
    stage       : str
    description : str
    date_update : Optional[datetime]

