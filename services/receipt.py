from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from repositories.receipt import ReceiptRepository
from repositories.sale import SaleRepository
from schemas.receipt import ReceiptCreate, ReceiptUpdate

receipt_repository = ReceiptRepository()
sale_repository = SaleRepository()


def get_receipt(db: Session, receipt_id: str):
    receipt = receipt_repository.get(db, receipt_id)
    if not receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found"
        )
    return receipt


def list_receipts(db: Session):
    return receipt_repository.get_all(db)


def create_receipt(db: Session, data: ReceiptCreate):
    if not sale_repository.get(db, data.sale_id):
        raise HTTPException(status_code=404, detail="Sale not found")
    if (
        db.query(receipt_repository.model)
        .filter(receipt_repository.model.sale_id == data.sale_id)
        .first()
    ):
        raise HTTPException(
            status_code=409, detail="A receipt already exists for this sale"
        )
    try:
        return receipt_repository.create(db, data.model_dump())
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="Receipt could not be created"
        ) from None


def update_receipt(db: Session, receipt_id: str, data: ReceiptUpdate):
    receipt = get_receipt(db, receipt_id)
    if data.sale_id and not sale_repository.get(db, data.sale_id):
        raise HTTPException(status_code=404, detail="Sale not found")
    try:
        return receipt_repository.update(
            db, receipt, data.model_dump(exclude_unset=True)
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="Receipt could not be updated"
        ) from None


def delete_receipt(db: Session, receipt_id: str):
    return receipt_repository.remove(db, get_receipt(db, receipt_id))
