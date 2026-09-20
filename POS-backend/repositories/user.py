from sqlalchemy.orm import Session
from models.user import UserModel


class UserRepository:
    def __init__(self):
        self.model = UserModel

    def get(self, db: Session, user_id: str):
        return db.query(self.model).filter(self.model.user_id == user_id).first()

    def get_by_username(self, db: Session, username: str):
        return db.query(self.model).filter(self.model.username == username).first()

    def get_by_email(self, db: Session, email: str):
        return db.query(self.model).filter(self.model.email == email).first()

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def create(self, db: Session, data: dict):
        user = self.model(**data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, db: Session, db_obj: UserModel, obj_in: dict):
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, db_obj: UserModel):
        db.delete(db_obj)
        db.commit()
        return db_obj