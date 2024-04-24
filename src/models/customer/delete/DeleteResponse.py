from pydantic import BaseModel

from typing import Optional

from models.customer.Customer import Customer

class DeleteResponse(BaseModel):
    Success: bool
    Customer: Optional[Customer]
    RowsAffected: Optional[int]
