from pydantic import BaseModel

from typing import Optional

from models.department.Department import Department

class CreateRequest(BaseModel):
    Name: str
    GroupName: str