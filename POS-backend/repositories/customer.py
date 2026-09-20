from sqlalchemy.orm import Session
from models.customer import CustomerModel


class CustomerRepository:
    def __init__(self):
        self.model = CustomerModel

    def get(self, db: Session, customer_id: str):
        return db.query(self.model).filter(self.model.customer_id == customer_id).first()

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def create(self, db: Session, data: dict):
        customer = self.model(**data)
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer

    def update(self, db: Session, db_obj: CustomerModel, obj_in: dict):
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, db_obj: CustomerModel):
        db.delete(db_obj)
        db.commit()
        return db_obj