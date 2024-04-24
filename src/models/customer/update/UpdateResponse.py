from pydantic import BaseModel

from typing import Optional

from models.customer.Customer import Customer

class UpdateResponse(BaseModel):
    Success: bool
    Customer: Optional[Customer]