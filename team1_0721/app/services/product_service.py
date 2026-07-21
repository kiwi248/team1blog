# product_service.py
from app.schemes.product_scheme import ProductCreate, ProductGet, ProductUpdate
from app.core.supabase_client import get_supabase

# 1. 입력
def product_create(product:ProductCreate) -> ProductGet:
    print("Database 에 입력이 처리 됩니다....")
    print(f"{product.name} {product.price}")
    return ProductGet(
        id="",
        name="",
        price=0,
        created_at=""
    )

# 2. 전체조회
def product_get_all() -> list[ProductGet]:
    result = [
        ProductGet(
            id="",
            name="",
            price=0,
            created_at=""
        )
    ];
    return result

# 3. 한개조회
def product_get(product_id:int) -> ProductGet:
    print("한개 조회 실행")
    return ProductGet(
            id="",
            name="",
            price=0,
            created_at=""
        )

# 4. 삭제
def product_delete(product_id:int) -> ProductGet:
    print("한개 수정 실행")
    return ProductGet(
            id="",
            name="",
            price=0,
            created_at=""
        )

# 5. 수정
def product_update(product:ProductUpdate) -> ProductGet:
    print("Database 에 수정이 처리 됩니다....")
    print(f"{product.name} {product.price}")
    return ProductGet(
            id="",
            name="",
            price=0,
            created_at=""
        )