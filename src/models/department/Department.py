from pydantic import BaseModel
from datetime import datetime

from ...sql.SqlDatabaseHandler import sqlDatabaseHandler as Database

from .delete import DeleteResponse
from .create import CreateRequest
from .create import CreateResponse
from .update import UpdateRequest
from .update import UpdateResponse

class Department(BaseModel):
    DepartmentID: int
    Name: str
    GroupName: str
    ModifiedDate: datetime
    
    @staticmethod
    def fromId(id: int):
        cursor = Database.getCursor()
        cursor.execute("SELECT * FROM HumanResources_Department WHERE DepartmentID = %s", (str(id),))
        department = cursor.fetchone()

        return Department(
            DepartmentID=department[0],
            Name=department[1],
            GroupName=department[2],
            ModifiedDate=department[3]
        )

    @staticmethod
    def delete(id: int):

        dept_cache = Department.fromId(id)

        if(dept_cache == None):
            return DeleteResponse(False, None, None)

        cursor = Database.getCursor()
        cursor.execute("DELETE FROM HumanResources_Department WHERE DepartmentID = %s", (str(id),))
        Database.commit()

        success = cursor.rowcount > 0

        return DeleteResponse(
            Success=success,
            Department=dept_cache, 
            RowsAffected=cursor.rowcount
            )
    
    @staticmethod
    def create(data: CreateRequest):
        cursor = Database.getCursor()

        next_id = Department.get_next_id()

        cursor.execute("INSERT IGNORE INTO HumanResources_Department (DepartmentID, Name, GroupName, ModifiedDate) VALUES(%s, %s, %s, %s)",
                           (next_id, data.Name, data.GroupName, datetime.now(),) 
                    )
        
        Database.commit()

        if(cursor.rowcount > 0):
            return CreateResponse(
                Success=True,
                Department=Department.fromId(next_id)
            )
        else:
            return CreateResponse(Success=False, Department=None)
    
    @staticmethod
    def update(id: int, data: UpdateRequest):
        cursor = Database.getCursor()

        cursor.execute("UPDATE HumanResources_Department SET GroupName = %s, ModifiedDate = NOW() WHERE DepartmentID = %s",
                       (data.GroupName, id))
        
        Database.commit()
        
        if(cursor.rowcount > 0):
            return UpdateResponse(
                Success=True,
                Department=Department.fromId(id)
            )
        else:
            return UpdateResponse(Success=False, Customer=None)
    
    @staticmethod
    def get_next_id():
        cursor = Database.getCursor()
        cursor.execute("SELECT MAX(DepartmentID) FROM HumanResources_Department")
        data = cursor.fetchone()

        return data[0] + 1