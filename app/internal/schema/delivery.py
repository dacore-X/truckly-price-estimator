from datetime import datetime

from pydantic import BaseModel


# Delivery Model for request validation
class Delivery(BaseModel):
    distance: float
    time: datetime
    type_id: int
    has_loader: bool
