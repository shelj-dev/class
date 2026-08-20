from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    description: str
    image: str

    class Config:
        from_attributes = True

