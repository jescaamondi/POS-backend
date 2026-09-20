from sqlalchemy.orm import Session
from models.payment import PaymentModel


class PaymentRepository:
    def __init__(self):
        self.model = PaymentModel

    def get(self, db: Session, payment_id: str):
        return db.query(self.model).filter(self.model.payment_id == payment_id).first()

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def create(self, db: Session, data: dict):
        payment = self.model(**data)
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    def update(self, db: Session, db_obj: PaymentModel, obj_in: dict):
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, db_obj: PaymentModel):
        db.delete(db_obj)
        db.commit()
        return db_obj