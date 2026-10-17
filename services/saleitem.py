from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories.product_repository import ProductRepository
from repositories.sale import SaleRepository
from repositories.saleitem import SaleItemRepository
from schemas.saleitem import SaleItemCreate, SaleItemUpdate

sale_item_repository = SaleItemRepository()
sale_repository = SaleRepository()
product_repository = ProductRepository()


def get_sale_item(db: Session, sale_item_id: str):
    item = sale_item_repository.get(db, sale_item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sale item not found"
        )
    return item


def _validate_references(db: Session, sale_id: str | None, product_id: str | None):
    if sale_id is not None and not sale_repository.get(db, sale_id):
        raise HTTPException(status_code=404, detail="Sale not found")
    if product_id is not None and not product_repository.get(db, product_id):
        raise HTTPException(status_code=404, detail="Product not found")


def list_sale_items(db: Session):
    return sale_item_repository.get_all(db)


def create_sale_item(db: Session, data: SaleItemCreate):
    _validate_references(db, data.sale_id, data.product_id)
    return sale_item_repository.create(db, data.model_dump())


def update_sale_item(db: Session, sale_item_id: str, data: SaleItemUpdate):
    item = get_sale_item(db, sale_item_id)
    _validate_references(db, data.sale_id, data.product_id)
    return sale_item_repository.update(db, item, data.model_dump(exclude_unset=True))


def delete_sale_item(db: Session, sale_item_id: str):
    return sale_item_repository.remove(db, get_sale_item(db, sale_item_id))
