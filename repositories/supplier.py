from sqlalchemy.orm import Session

from models.supplier import SupplierModel


class SupplierRepository:
    def __init__(self):
        self.model = SupplierModel

    def get(self, db: Session, supplier_id: str):
        return (
            db.query(self.model).filter(self.model.supplier_id == supplier_id).first()
        )

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def create(self, db: Session, data: dict):
        supplier = self.model(**data)
        db.add(supplier)
        db.commit()
        db.refresh(supplier)
        return supplier

    def update(self, db: Session, db_obj: SupplierModel, obj_in: dict):
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, db_obj: SupplierModel):
        db.delete(db_obj)
        db.commit()
        return db_obj
