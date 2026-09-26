from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from pydantic import BaseModel


app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    data = Column(String, index=True)
 
    
Base.metadata.create_all(bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        

class UserCreate(BaseModel):
    username: str
    email: str
    hashed_password: str
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: str


@app.post("/users/create/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email, hashed_password=user.hashed_password)
    if (db.query(User).filter(User.username == user.username).first() 
                        or 
        db.query(User).filter(User.email == user.email).first()):
        raise HTTPException(
            status_code=400,
            detail="Username or email already registered"
        )    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/", response_model=list[UserResponse])
def users(db: Session = Depends(get_db)):
    db_user = db.query(User).all()
    return db_user


@app.get("/users/{user_id}/", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/login/", response_model=UserResponse)
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user or db_user.hashed_password != password:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return db_user


class ItemCreate(BaseModel):
    title: str
    data: str


class ItemResponse(BaseModel):
    id: int
    title: str
    data: str


# -------------------------
# CREATE
# -------------------------

@app.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):

    db_item = Item(
        title=item.title,
        data=item.data
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


# -------------------------
# READ ALL
# -------------------------

@app.get("/items/", response_model=list[ItemResponse])
def get_items(db: Session = Depends(get_db)):

    items = db.query(Item).all()

    return items


# -------------------------
# READ ONE
# -------------------------

@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):

    item = db.query(Item).filter(Item.id == item_id).first()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return item


# -------------------------
# UPDATE
# -------------------------

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    item_data: ItemCreate,
    db: Session = Depends(get_db)
):

    item = db.query(Item).filter(Item.id == item_id).first()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    item.title = item_data.title
    item.data = item_data.data

    db.commit()
    db.refresh(item)

    return item


# -------------------------
# DELETE
# -------------------------

@app.delete("/items/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db)
):

    item = db.query(Item).filter(Item.id == item_id).first()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    db.delete(item)
    db.commit()

    return {
        "message": "Item deleted successfully"
    }
    