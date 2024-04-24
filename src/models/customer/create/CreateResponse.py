from pydantic import BaseModel

from typing import Optional

from customer.Customer import Customer

class CreateResponse(BaseModel):
    Success: bool
    Customer: Optional[Customer]