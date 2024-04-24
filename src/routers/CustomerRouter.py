from fastapi import APIRouter
from datetime import datetime

from pydantic import BaseModel

from ..models.customer.Customer import Customer

from ..models.customer.delete import DeleteResponse
from ..models.customer.create import CreateRequest
from ..models.customer.create import CreateResponse
from ..models.customer.update import UpdateRequest
from ..models.customer.update import UpdateResponse

router_customer = APIRouter(prefix="/api/v1/customer")

@router_customer.get(
        "/{id}",
        response_model=Customer
        )
def get_user(id: int):
    return Customer.fromId(id)

@router_customer.delete(
    "/{id}",
    response_model=DeleteResponse
    )
def delete_user(id: int):
    return Customer.delete(id)


@router_customer.post(
    "/",
    response_model=CreateResponse
    )
def create_customer(data: CreateRequest):
    return Customer.create(data)

@router_customer.put(
    "/{id}",
    response_model=UpdateResponse
    )
def update_customer(customer_id: int, customer: UpdateRequest):
    return Customer.update(customer_id, customer)
