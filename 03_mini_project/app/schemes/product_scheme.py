# product_scheme.py
from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name:str
    price:int

class ProductUpdate(BaseModel):
    id:str
    name:str
    price:int

class ProductGet(BaseModel):
    id:str
    name:str
    price:int
    created_at:str