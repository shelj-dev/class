from pydantic import BaseModel


class Product(BaseModel):
    id:int
    name:str
    
    class Config:
        from_attributes = True
