def main():
    print("Hello from files!")


if __name__ == "__main__":
    main()

from fastapi import FastAPI
from models import Product

app=FastAPI()

@app.get("/")
def root():
    return{"message":"hello all"}

products=[
    Product(id=1,name="phone",description="Buget phone",price=66.00,quantity=2),
    Product(id=2,name="laptop",description="Buget laptop",price=67.00,quantity=20),
    Product(id=3,name="pen",description="a black pen",price=75.00,quantity=2),
    Product(id=4,name="table",description="A wooden table",price=86.00,quantity=4),
]

@app.get("/products")
def get_all_products():
    return products

@app.get("/products/{id}")
def get_all_product_by_id(id:int):
    for product in products:
        if product.id==id:
            return product
    return "not found"

@app.post("/products")
def add_product(product:Product):
    products.append(product)
    return product

@app.put("/product")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "Product Updated Successfully"

@app.delete("/product")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "Product Deleted Successfully"

    return "Product not found"



