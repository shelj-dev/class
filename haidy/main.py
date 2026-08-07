from fastapi import (
    FastAPI,
    Depends
)

from sqlalchemy.orm import Session
import schemas 
from haidy.models import Product
from haidy.database import (
    engine,
    SessionLocal
)


app = FastAPI()

schemas.Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message":"ok"}

@app.get("/hello")
def hello():
    return {"message":"hello"}

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@app.post("/products/db")
def add_products_db(product: Product, db: Session = Depends(get_db)):
    new_product = schemas.Product(
        id=product.id,
        name=product.name
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return {
        "message":"Product added successfully",
        "data": new_product
    }


@app.get("/products/db/{id}")
def get_product_db(id: int, db: Session = Depends(get_db)):
    product = db.query(schemas.Product).filter(schemas.Product.id == id).first()
    
    if product is None:
        return {
            "message":"Product not found"
        }
    return product


@app.put("/products/db/{id}")
def update_product_db(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(schemas.Product).filter(schemas.Product.id == id).first()
    
    if db_product is None:
        return {
            "message":"Product not found"
        }
        
    db_product.name = product.name
    db.commit()
    db.refresh(db_product)
    
    return {
        "message":"Product updated successfully",
        "data": db_product
    }
    

@app.delete("/products/db/{id}")
def delete_product_db(id: int, db: Session = Depends(get_db)):
    db_product = db.query(schemas.Product).filter(schemas.Product.id == id).first()
    
    if db_product is None:
        return {
            "message":"Product not found"
        }
        
    db.delete(db_product)
    db.commit()
    
    return {
        "message":"Product deleted successfully"
    }