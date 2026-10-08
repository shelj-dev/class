from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def root():
    return{"message":"hello"}



import os
import shutil

UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
    
    
from fastapi.staticfiles import StaticFiles

app.mount(
    "/files",
    StaticFiles(directory=UPLOAD_DIR),
    name="files"
)


from fastapi import UploadFile, File, HTTPException

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):

    filename = file.filename

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="File not selected"
        )

    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "message": "File Uploaded Successfully",
        "fileName": filename,
        "file_url": f"http://127.0.0.1:8000/files/{filename}"
    }
    
    
from pydantic import BaseModel

class ProductCreate(BaseModel):

    name: str
    description: str
    image: str

    class Config:
        from_attributes = True
        
        

from sqlalchemy import Column, Integer, String



from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./products.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


from sqlalchemy.orm import Session
from fastapi import Depends

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

class Products(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    image = Column(String)
    
    
@app.post("/products/db")
def add_product_db(
    product: ProductCreate,
    db: Session = Depends(get_db)
):

    new_product = Products(
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
    
    
