from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String
)
from haidy.database import Base


class Product(Base):
    __tablename__="products"
    
    user_id=Column(Integer, primary_key=True, index=True)
    title=Column(String)
    is_completed=Column(Boolean, default=False)
