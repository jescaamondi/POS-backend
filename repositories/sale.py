from sqlalchemy.orm import Session

from models.sale import SaleModel


class SaleRepository:
    def __init__(self):
        self.model = SaleModel

    def get(self, db: Session, sale_id: str):
        return db.query(self.model).filter(self.model.sale_id == sale_id).first()

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def create(self, db: Session, data: dict):
        sale = self.model(**data)
        db.add(sale)
        db.commit()
        db.refresh(sale)
        return sale

    def update(self, db: Session, db_obj: SaleModel, obj_in: dict):
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, db_obj: SaleModel):
        db.delete(db_obj)
        db.commit()
        return db_obj
