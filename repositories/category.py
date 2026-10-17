from sqlalchemy.orm import Session

from models.category import CategoryModel


class CategoryRepository:
    def __init__(self):
        self.model = CategoryModel

    def get(self, db: Session, category_id: str):
        return (
            db.query(self.model).filter(self.model.category_id == category_id).first()
        )

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def create(self, db: Session, data: dict):
        category = self.model(**data)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    def update(self, db: Session, db_obj: CategoryModel, obj_in: dict):
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, db_obj: CategoryModel):
        db.delete(db_obj)
        db.commit()
        return db_obj
