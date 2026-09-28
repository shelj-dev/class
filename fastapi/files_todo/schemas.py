from pydantic import BaseModel

class ProductCreate(BaseModel):
    id: int
    name: str
    description: str
    image: str

    class Config:
        from_attributes = True