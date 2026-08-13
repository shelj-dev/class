def main():
    print("Hello from files!")


if __name__ == "__main__":
    main()

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import schemas
from models import Product
from database import engine, SessionLocal



app=FastAPI()

schemas.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return{"message":"hello all"}

products=[
    Product(id=1,name="phone",description="Buget phone",image=""),
    Product(id=2,name="laptop",description="Buget laptop",image=""),
    Product(id=3,name="pen",description="a black pen",image=""),
    Product(id=4,name="table",description="A wooden table",image=""),
]

@app.get("/products")
def get_all_products():
    return products

@app.get("/products/{id}")
def get_all_product_by_id(id:int):
    for product in products:
        if product.id==id:
            return product
    return "not found"

@app.post("/products")
def add_product(product:Product):
    products.append(product)
    return product

@app.put("/product")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "Product Updated Successfully"

@app.delete("/product")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "Product Deleted Successfully"

    return "Product not found"

#add product for database

@app.post("/products/db")
def add_product_db(product: Product, db: Session = Depends(get_db)):
    new_product = schemas.Product(
        id=product.id,
        name=product.name,
        description=product.description,
        image=product.image
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "Product Added Successfully",
        "data": new_product
    }

#get product for database
@app.get("/products/db/{id}")
def get_product_db(id: int, db: Session = Depends(get_db)):
    product = db.query(schemas.Product).filter(schemas.Product.id == id).first()

    if product is None:
        return {"message": "Product not found"}

    return product

#put product for database
@app.put("/products/db/{id}")
def update_product_db(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(schemas.Product).filter(schemas.Product.id == id).first()

    if db_product is None:
        return {"message": "Product not found"}

    db_product.name = product.name
    db_product.description = product.description

    db.commit()
    db.refresh(db_product)

    return {
        "message": "Product Updated Successfully",
        "data": db_product
    }

#delete product for database
@app.delete("/products/db/{id}")
def delete_product_db(id: int, db: Session = Depends(get_db)):
    db_product = db.query(schemas.Product).filter(schemas.Product.id == id).first()
    if db_product is None:
        return {"message": "Product not found"}

    db.delete(db_product)
    db.commit()

    return {"message": "Product Deleted Successfully"}
