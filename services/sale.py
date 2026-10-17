from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories.customer import CustomerRepository
from repositories.sale import SaleRepository
from repositories.user import UserRepository
from schemas.sale import SaleCreate, SaleUpdate

sale_repository = SaleRepository()
user_repository = UserRepository()
customer_repository = CustomerRepository()


def get_sale(db: Session, sale_id: str):
    sale = sale_repository.get(db, sale_id)
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found"
        )
    return sale


def _validate_references(db: Session, user_id: str | None, customer_id: str | None):
    if user_id is not None and not user_repository.get(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    if customer_id is not None and not customer_repository.get(db, customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")


def list_sales(db: Session):
    return sale_repository.get_all(db)


def create_sale(db: Session, data: SaleCreate):
    _validate_references(db, data.user_id, data.customer_id)
    return sale_repository.create(db, data.model_dump())


def update_sale(db: Session, sale_id: str, data: SaleUpdate):
    sale = get_sale(db, sale_id)
    _validate_references(db, data.user_id, data.customer_id)
    return sale_repository.update(db, sale, data.model_dump(exclude_unset=True))


def delete_sale(db: Session, sale_id: str):
    return sale_repository.remove(db, get_sale(db, sale_id))
