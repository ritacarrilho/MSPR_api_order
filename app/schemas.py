from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderBase(BaseModel):
    customerId: int
    createdAt: datetime
    updated_at: datetime
    status: int


class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id_order: int

    class Config:
        orm_mode = True

class OrderProductBase(BaseModel):
    productId: int
    quantity: int
    id_order: int

class OrderProductCreate(OrderProductBase):
    pass

class OrderProduct(OrderProductBase):
    id_order_products: int

    class Config:
        orm_mode = True
        
class OrderCreate(BaseModel):
    customerId: int
    createdAt: datetime
    updated_at: datetime
    status: int

class OrderProductCreate(BaseModel):
    productId: int
    quantity: int
    id_order: int
    
class OrderUpdate(BaseModel):
    customerId: Optional[int] = None
    createdAt: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status: Optional[int] = None

class OrderProductUpdate(BaseModel):
    productId: Optional[int] = None
    quantity: Optional[int] = None
    id_order: Optional[int] = None


class CustomerOrder(BaseModel):
    id_order: int
    createdAt: datetime
    updated_at: datetime
    status: int

class CustomerOrdersResponse(BaseModel):
    customer_id: int
    orders: List[CustomerOrder]

    class Config:
        orm_mode = True