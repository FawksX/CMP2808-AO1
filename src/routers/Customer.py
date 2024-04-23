from fastapi import APIRouter
from datetime import datetime

from pydantic import BaseModel

from ..models.Customer import Customer

router_customer = APIRouter(prefix="/api/v1/customer")

@router_customer.get(
        "/{id}",
        response_model=Customer
        )
def get_user(id: int):
    return Customer.fromId(id)

@router_customer.delete(
    "/{id}",
    response_model=Customer.Delete
    )
def delete_user(id: int):
    return Customer.delete(id)


@router_customer.post(
    "/",
    response_model=Customer
    )
def create_customer(data: Customer.Create):
    try:
        return Customer.create(data)
    except Exception as exception:
        print(exception)

@router_customer.put(
    "/{id}",
    response_model=Customer
    )
def update_customer(customer_id: int, customer: Customer.Update):
    return Customer.update(customer_id, customer)
