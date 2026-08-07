from pydantic import BaseModel

class product(BaseModel):
    id:int
    name:str

    class config:
        from_attributes=True