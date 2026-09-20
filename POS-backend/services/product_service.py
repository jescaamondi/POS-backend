from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.category import CategoryRepository
from repositories.product_repository import ProductRepository
from repositories.supplier import SupplierRepository
from schemas.product import ProductCreate, ProductUpdate

product_repository = ProductRepository()
category_repository = CategoryRepository()
supplier_repository = SupplierRepository()


def get_product(db: Session, product_id: str):
    product = product_repository.get(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


def _validate_references(db: Session, category_id: str | None, supplier_id: str | None):
    if category_id is not None and not category_repository.get(db, category_id):
        raise HTTPException(status_code=404, detail="Category not found")
    if supplier_id is not None and not supplier_repository.get(db, supplier_id):
        raise HTTPException(status_code=404, detail="Supplier not found")


def list_products(db: Session):
    return product_repository.get_all(db)


def create_product(db: Session, data: ProductCreate):
    _validate_references(db, data.category_id, data.supplier_id)
    return product_repository.create(db, data.model_dump())


def update_product(db: Session, product_id: str, data: ProductUpdate):
    get_product(db, product_id)
    _validate_references(db, data.category_id, data.supplier_id)
    return product_repository.update(db, product_repository.get(db, product_id), data.model_dump(exclude_unset=True))


def delete_product(db: Session, product_id: str):
    return product_repository.remove(db, get_product(db, product_id))
