from pydantic import BaseModel
from typing import Optional
from datetime import datetime

import uuid

from .delete import DeleteResponse
from .create import CreateRequest
from .create import CreateResponse
from .update import UpdateRequest
from .update import UpdateResponse

from fastapi import HTTPException

from ...sql.SqlDatabaseHandler import sqlDatabaseHandler as Database

class Customer(BaseModel):
    CustomerID: int
    PersonID: Optional[int] = None
    StoreID: Optional[int] = None
    TerritoryID: Optional[int] = None
    AccountNumber: str
    rowguid: str
    ModifiedDate: datetime

    @staticmethod
    def fromId(customer_id: int):
        cursor = Database.getCursor()
        cursor.execute("SELECT * FROM Sales_Customer WHERE CustomerID = %s", (str(customer_id),))

        user = cursor.fetchone()

        return Customer(
            CustomerID=user[0],
            PersonID=user[1],
            StoreID=user[2],
            TerritoryID=user[3],
            AccountNumber=user[4],
            rowguid=user[5],
            ModifiedDate=user[6]
        )
    
    @staticmethod
    def delete(customer_id: int):

        customer_cache = Customer.fromId(customer_id)

        if(customer_cache == None):
            raise HTTPException(
                status_code=404,
                content={"message": f"Could not find Customer {customer_id}"}
            )

        cursor = Database.getCursor()
        cursor.execute("DELETE FROM Sales_Customer WHERE CustomerID = %s", (str(customer_id),))
        Database.commit()

        if cursor.rowcount > 0:
            return DeleteResponse(
                Success=True,
                Customer=customer_cache, 
                RowsAffected=cursor.rowcount
                )
    
    @staticmethod
    def create(data: CreateRequest):
        cursor = Database.getCursor()
        next_id = Customer.get_next_id()
        accounting_number = Customer.generate_accounting_number(next_id)
        rowguid = str(uuid.uuid4())

        cursor.execute("INSERT INTO Sales_Customer (CustomerID, AccountNumber, rowguid, ModifiedDate) VALUES(%s, %s, %s, %s)",
                (next_id, accounting_number, rowguid, datetime.now(),)
        )
        Database.commit()

        if(cursor.rowcount > 0):
            return CreateResponse(
                Success=True,
                Customer=Customer.fromId(next_id)
            )
        else:
            return CreateResponse(Success=False, Customer=None)
        
    @staticmethod
    def update(customerId: int, customer: UpdateRequest):
        cursor = Database.getCursor()

        cursor.execute("UPDATE Sales_Customer SET PersonID = %s, StoreID = %s, TerritoryID = %s, AccountNumber = %s, ModifiedDate = NOW() WHERE CustomerID = %s",
                           (customer.PersonID, customer.StoreID, customer.TerritoryID, customer.AccountNumber, customerId,))
        
        Database.commit()

        if(cursor.rowcount > 0):
            return UpdateResponse(
                Success=True, 
                Customer=Customer.fromId(customerId)
                )
        else:
            return UpdateResponse(Success=False, Customer=None)

    
    @staticmethod
    def get_next_id():
        cursor = Database.getCursor()
        cursor.execute("SELECT MAX(CustomerID) FROM Sales_Customer")
        data = cursor.fetchone()

        return data[0] + 1
    
    @staticmethod
    def generate_accounting_number(next_id: int):
        return "AW" + ("0" * (8 - len(str(next_id)))) + str(next_id)