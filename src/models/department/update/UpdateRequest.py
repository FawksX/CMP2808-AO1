from pydantic import BaseModel

from typing import Optional

from models.department.Department import Department

class UpdateRequest(BaseModel):
    GroupName: str