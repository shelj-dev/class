from pydantic import BaseModel

class ProductCreate(BaseModel):
    id: int | None = None
    name: str
    description: str
    image: str

    class Config:
        from_attributes = True