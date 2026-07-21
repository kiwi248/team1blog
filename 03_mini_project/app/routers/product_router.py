# product_router.py

from fastapi import APIRouter
from app.schemes.product_scheme import * 
from app.services.product_service import *

product_router = APIRouter()

# 1. create
@product_router.post("/product/create")
def create(product:ProductCreate) -> ProductGet:
    """  """
    return product_create(product)

# 2. 한개 조회
@product_router.get("/product/get/{product_id}")
def get(product_id:int) -> ProductGet:
    return product_get(product_id)

# 3. 전체 조회
@product_router.get("/product/getall")
def get_all() -> list[ProductGet]:
    return product_get_all()

# 4. 한개 삭제
@product_router.delete("/product/delete/{product_id}")
def delete(product_id:int) -> ProductGet:
    return product_delete(product_id)

# 5. 수정
@product_router.put("/product/put")
def put(product:ProductUpdate) -> ProductGet:
    """  """
    return product_update(product)