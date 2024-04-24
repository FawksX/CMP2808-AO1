from pydantic import BaseModel

from typing import Optional

from models.customer.Customer import Customer

class Create(BaseModel):
    PersonID: Optional[int] = None
    StoreID: Optional[int] = None
    TerritoryID: Optional[int] = None