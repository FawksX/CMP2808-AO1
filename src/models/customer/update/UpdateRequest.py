
from pydantic import BaseModel

from typing import Optional

from models.customer.Customer import Customer

class UpdateRequest(BaseModel):
    PersonID: Optional[int] = None
    StoreID: Optional[int] = None
    TerritoryID: Optional[int] = None
    AccountNumber: Optional[str] = None