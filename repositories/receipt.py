from sqlalchemy.orm import Session

from models.receipt import ReceiptModel


class ReceiptRepository:
    def __init__(self):
        self.model = ReceiptModel

    def get(self, db: Session, receipt_id: str):
        return db.query(self.model).filter(self.model.receipt_id == receipt_id).first()

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def create(self, db: Session, data: dict):
        receipt = self.model(**data)
        db.add(receipt)
        db.commit()
        db.refresh(receipt)
        return receipt

    def update(self, db: Session, db_obj: ReceiptModel, obj_in: dict):
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, db_obj: ReceiptModel):
        db.delete(db_obj)
        db.commit()
        return db_obj
