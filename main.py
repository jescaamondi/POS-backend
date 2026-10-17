from fastapi import Depends, FastAPI

from core.dependencies import get_current_user
from routers import (
    auth,
    category,
    customer,
    payment,
    products,
    receipt,
    sale,
    saleitem,
    supplier,
    user,
)

app = FastAPI(title="POS API", version="1.0.0")

app.include_router(auth.router)

protected = [Depends(get_current_user)]

app.include_router(products.router, dependencies=protected)
app.include_router(customer.router, dependencies=protected)
app.include_router(user.router, dependencies=protected)
app.include_router(sale.router, dependencies=protected)
app.include_router(saleitem.router, dependencies=protected)
app.include_router(payment.router, dependencies=protected)
app.include_router(category.router, dependencies=protected)
app.include_router(supplier.router, dependencies=protected)
app.include_router(receipt.router, dependencies=protected)


@app.get("/")
def root():
    return {"My POS": "Welcome to the Point of Sale System API."}
