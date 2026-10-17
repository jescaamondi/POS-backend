from fastapi import FastAPI

from routers import (
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

app.include_router(products.router)
app.include_router(customer.router)
app.include_router(user.router)
app.include_router(sale.router)
app.include_router(saleitem.router)
app.include_router(payment.router)
app.include_router(category.router)
app.include_router(supplier.router)
app.include_router(receipt.router)


@app.get("/")
def root():
    return {"My POS": "Welcome to the Point of Sale System API."}
