from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from repositories.payment import PaymentRepository
from repositories.sale import SaleRepository
from schemas.payment import PaymentCreate, PaymentUpdate

payment_repository = PaymentRepository()
sale_repository = SaleRepository()


def get_payment(db: Session, payment_id: str):
    payment = payment_repository.get(db, payment_id)
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    return payment


def list_payments(db: Session):
    return payment_repository.get_all(db)


def create_payment(db: Session, data: PaymentCreate):
    if not sale_repository.get(db, data.sale_id):
        raise HTTPException(status_code=404, detail="Sale not found")
    if db.query(payment_repository.model).filter(payment_repository.model.sale_id == data.sale_id).first():
        raise HTTPException(status_code=409, detail="A payment already exists for this sale")
    try:
        return payment_repository.create(db, data.model_dump())
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Payment could not be created") from None


def update_payment(db: Session, payment_id: str, data: PaymentUpdate):
    payment = get_payment(db, payment_id)
    if data.sale_id and not sale_repository.get(db, data.sale_id):
        raise HTTPException(status_code=404, detail="Sale not found")
    try:
        return payment_repository.update(db, payment, data.model_dump(exclude_unset=True))
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Payment could not be updated") from None


def delete_payment(db: Session, payment_id: str):
    return payment_repository.remove(db, get_payment(db, payment_id))
