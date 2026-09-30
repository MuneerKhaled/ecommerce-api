from sqlalchemy.orm import Session

from . import models
from .schemas import ProductCreate


def get_products(db: Session):
    return db.query(models.Product).all()


def get_product(db: Session, product_id: int):
    return (
        db.query(models.Product)
        .filter(models.Product.id == product_id)
        .first()
    )


def create_product(db: Session, product: ProductCreate):
    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)

    if product:
        db.delete(product)
        db.commit()

    return product