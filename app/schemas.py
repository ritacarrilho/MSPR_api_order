from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderBase(BaseModel):
    customerId: int
    createdAt: datetime

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

class OrderProductCreate(BaseModel):
    productId: int
    quantity: int
    id_order: int