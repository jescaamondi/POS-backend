from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.category import CategoryRepository
from schemas.category import CategoryCreate, CategoryUpdate

category_repository = CategoryRepository()


def get_category(db: Session, category_id: str):
    category = category_repository.get(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category

def list_categories(db: Session):
    return category_repository.get_all(db)


def create_category(db: Session, data: CategoryCreate):
    return category_repository.create(db, data.model_dump())


def update_category(db: Session, category_id: str, data: CategoryUpdate):
    category = get_category(db, category_id)
    return category_repository.update(db, category, data.model_dump(exclude_unset=True))


def delete_category(db: Session, category_id: str):
    category = get_category(db, category_id)
    return category_repository.remove(db, category)