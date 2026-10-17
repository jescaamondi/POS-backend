from sqlalchemy.orm import Session

from models.product import ProductModel


class ProductRepository:
    def __init__(self):
        self.model = ProductModel

    def get(self, db: Session, product_id: str):
        return db.query(self.model).filter(self.model.product_id == product_id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, data: dict):
        db_product = self.model(**data)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    def update(self, db: Session, db_obj: ProductModel, obj_in: dict):
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, db_obj: ProductModel):
        db.delete(db_obj)
        db.commit()
        return db_obj
