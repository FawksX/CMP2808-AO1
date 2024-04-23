from pydantic import BaseModel
from datetime import datetime

from ..sql.SqlDatabaseHandler import sqlDatabaseHandler as Database

class Department(BaseModel):
    DepartmentID: int
    Name: str
    GroupName: str
    ModifiedDate: datetime

    class Delete(BaseModel):
        DepartmentID: int
        RowsAffected: int
    
    class Update(BaseModel):
        GroupName: str
    
    class Create(BaseModel):
        Name: str
        GroupName: str
    
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
        cursor = Database.getCursor()
        cursor.execute("DELETE FROM HumanResources_Department WHERE DepartmentID = %s", (str(id),))
        Database.commit()
        return Department.Delete(
            DepartmentID=id, 
            RowsAffected=cursor.rowcount
            )
    
    @staticmethod
    def create(data: Create):
        cursor = Database.getCursor()

        next_id = Department.get_next_id()

        cursor.execute("INSERT IGNORE INTO HumanResources_Department (DepartmentID, Name, GroupName, ModifiedDate) VALUES(%s, %s, %s, %s)",
                           (next_id, data.Name, data.GroupName, datetime.now(),) 
                    )
        
        Database.commit()

        if(cursor.rowcount > 0):
            return Department.fromId(next_id)
        else:
            return None
    
    @staticmethod
    def update(id: int, data: Update):
        cursor = Database.getCursor()

        cursor.execute("UPDATE HumanResources_Department SET GroupName = %s, ModifiedDate = NOW() WHERE DepartmentID = %s",
                       (data.GroupName, id))
        
        Database.commit()
        return Department.fromId(id)
    
    @staticmethod
    def get_next_id():
        cursor = Database.getCursor()
        cursor.execute("SELECT MAX(DepartmentID) FROM HumanResources_Department")
        data = cursor.fetchone()

        return data[0] + 1