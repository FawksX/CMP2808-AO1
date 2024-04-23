from fastapi import FastAPI

from .routers.Customer import router_customer
from .routers.Department import router_departments

app = FastAPI()

routers = [
    router_customer,
    router_departments
]

for router in routers:
    app.include_router(router)

@app.get("/")
async def read_root():
    return {"status": "OK"}