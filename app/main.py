from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.models import Base, Product, User, Order, Account, EAN, SKU
from app.database import SessionLocal, get_db, engine

app = FastAPI(title="WMS Operacional API", version="1.0.0")


# Pydantic models for API
class ProductCreate(BaseModel):
    name: str = Field(..., description="Nome do produto")
    sku: str = Field(..., description="Código SKU")
    ean: str = Field(..., description="Código EAN de 13 dígitos")
    price: float = Field(..., description="Preço do produto")
    quantity: int = Field(default=0, description="Quantidade em estoque")


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Nome do produto")
    sku: Optional[str] = Field(None, description="Código SKU")
    ean: Optional[str] = Field(None, description="Código EAN de 13 dígitos")
    price: Optional[float] = Field(None, description="Preço do produto")
    quantity: Optional[int] = Field(None, description="Quantidade em estoque")


class ProductResponse(BaseModel):
    id: int
    name: str
    sku: str
    ean: str
    price: float
    quantity: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., max_length=100)
    full_name: str = Field(..., max_length=100)
    password: str = Field(..., min_length=6)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    is_active: bool
    is_superuser: bool
    created_at: datetime

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    user_id: int
    items: List[dict] = Field(..., description="Lista de itens {product_id, quantity}")
    shipping_address: Optional[str] = Field(None, description="Endereço de entrega")


class OrderResponse(BaseModel):
    id: int
    order_code: str
    user_id: int
    status: str
    total_amount: float
    created_at: datetime
    shipping_address: Optional[str]

    class Config:
        from_attributes = True


@app.on_event("startup")
async def startup():
    """Create database tables on startup."""
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "WMS Operacional API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


# Product endpoints
@app.post("/products/", response_model=ProductResponse)
async def create_product(product: ProductCreate, db = Depends(get_db)):
    db_product = Product(
        name=product.name,
        sku=product.sku,
        ean=product.ean,
        price=product.price,
        quantity=product.quantity,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.get("/products/", response_model=List[ProductResponse])
async def list_products(db = Depends(get_db)):
    products = db.query(Product).all()
    return products


@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product


@app.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product: ProductUpdate, db = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.delete("/products/{product_id}")
async def delete_product(product_id: int, db = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(db_product)
    db.commit()
    return {"message": "Produto removido"}


# User endpoints
@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db = Depends(get_db)):
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/", response_model=List[UserResponse])
async def list_users(db = Depends(get_db)):
    users = db.query(User).all()
    return users


# Order endpoints
@app.post("/orders/", response_model=OrderResponse)
async def create_order(order: OrderCreate, db = Depends(get_db)):
    # Calculate total
    total = 0
    for item in order.items:
        product = db.query(Product).filter(Product.id == item["product_id"]).first()
        if product:
            total += product.price * item["quantity"]
    
    db_order = Order(
        order_code=f"ORG-{uuid.uuid4().hex[:6].upper()}",
        user_id=order.user_id,
        status="pending",
        total_amount=total,
        shipping_address=order.shipping_address,
    )
    db.add(db_order)
    
    # Reduzir estoque
    for item in order.items:
        product = db.query(Product).filter(Product.id == item["product_id"]).first()
        if product:
            product.quantity = max(0, product.quantity - item["quantity"])
    
    db.commit()
    db.refresh(db_order)
    return db_order


@app.get("/orders/", response_model=List[OrderResponse])
async def list_orders(db = Depends(get_db)):
    orders = db.query(Order).all()
    return orders


@app.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return order


# Import uuid at module level
import uuid

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)