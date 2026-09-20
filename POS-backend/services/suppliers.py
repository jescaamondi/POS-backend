from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.supplier import SupplierRepository
from schemas.supplier import SupplierCreate, SupplierUpdate

supplier_repository = SupplierRepository()


def get_supplier(db: Session, supplier_id: str):
    supplier = supplier_repository.get(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
    return supplier


def list_suppliers(db: Session):
    return supplier_repository.get_all(db)


def create_supplier(db: Session, data: SupplierCreate):
    return supplier_repository.create(db, data.model_dump())


def update_supplier(db: Session, supplier_id: str, data: SupplierUpdate):
    return supplier_repository.update(db, get_supplier(db, supplier_id), data.model_dump(exclude_unset=True))


def delete_supplier(db: Session, supplier_id: str):
    return supplier_repository.remove(db, get_supplier(db, supplier_id))
