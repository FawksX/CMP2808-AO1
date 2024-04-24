from pydantic import BaseModel

from typing import Optional

from models.department.Department import Department

class DeleteResponse(BaseModel):
    Success: bool
    Department: Optional[Department]
    RowsAffected: Optional[int]
