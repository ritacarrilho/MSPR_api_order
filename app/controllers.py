from sqlalchemy.orm import Session
from .models import Order, OrderProduct
from fastapi import HTTPException
from . import schemas

def get_all_orders(db: Session):
    return db.query(Order).all()

def get_order_by_id(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id_order == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def get_all_order_products(db: Session):
    return db.query(OrderProduct).all()

def get_order_product_by_id(db: Session, order_product_id: int):
    order_product = db.query(OrderProduct).filter(OrderProduct.id_order_products == order_product_id).first()
    if order_product is None:
        raise HTTPException(status_code=404, detail="OrderProduct not found")
    return order_product