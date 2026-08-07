from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean
)
from database import Base


class Product(Base):
    __tablename__="products"
    
    user_id=Column(Integer, primary_key=True, index=True)
    title=Column(String)
    is_completed = Column(Boolean, default=False)