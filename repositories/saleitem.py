from sqlalchemy.orm import Session

from models.saleitem import SaleItemModel


class SaleItemRepository:
    def __init__(self):
        self.model = SaleItemModel

    def get(self, db: Session, sale_item_id: str):
        return (
            db.query(self.model).filter(self.model.sale_item_id == sale_item_id).first()
        )

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def create(self, db: Session, data: dict):
        sale_item = self.model(**data)
        db.add(sale_item)
        db.commit()
        db.refresh(sale_item)
        return sale_item

    def update(self, db: Session, db_obj: SaleItemModel, obj_in: dict):
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, db_obj: SaleItemModel):
        db.delete(db_obj)
        db.commit()
        return db_obj
