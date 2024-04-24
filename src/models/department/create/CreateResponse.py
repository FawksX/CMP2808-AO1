from pydantic import BaseModel

from typing import Optional

from models.department.Department import Department

class CreateResponse(BaseModel):
    Success: bool
    Department: Optional[Department]