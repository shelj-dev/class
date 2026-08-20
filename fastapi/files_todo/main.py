def main():
    print("Hello from files!")


if __name__ == "__main__":
    main()

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import schemas
from models import product
from database import engine, SessionLocal



app=FastAPI()

schemas.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
products=[
    product(id=1,name="bag"),
    product(id=2,name="pen")
]
@app.get("/hello")
def root():
    return{"message":"hello"}

@app.get("/product")
def add_product():
    return products

@app.post("/products/db")
def add_product_db(product: product, db: Session = Depends(get_db)):
    new_product = schemas.Product(
        id=product.id,
        name=product.name
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "Product Added Successfully",
        "data": new_product
    }

@app.get("/products/db/{id}")
def get_product_db(id: int, db: Session = Depends(get_db)):
    product = db.query(schemas.Product).filter(schemas.Product.id == id).first()

    if product is None:
        return {"message": "Product not found"}

    return product

@app.put("/products/db/{id}")
def update_product_db(id: int, product: product, db: Session = Depends(get_db)):
    db_product = db.query(schemas.Product).filter(schemas.Product.id == id).first()

    if db_product is None:
        return {"message": "Product not found"}

    db_product.name = product.name
    # db_product.description = product.description

    db.commit()
    db.refresh(db_product)

    return {
        "message": "Product Updated Successfully",
        "data": db_product
    }

@app.delete("/products/db/{id}")
def delete_product_db(id: int, db: Session = Depends(get_db)):
    db_product = db.query(schemas.Product).filter(schemas.Product.id == id).first()

    if db_product is None:
        return {"message": "Product not found"}

    db.delete(db_product)
    db.commit()

    return {"message": "Product Deleted Successfully"}