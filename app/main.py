from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List 
from . import controllers, schemas
from .database import get_db

app = FastAPI(
    title="Paye ton kawa",
    description="Le café c'est la vie",
    summary="API Commandes",
    version="0.0.2",
)

@app.get("/orders/", response_model=List[schemas.Order], tags=["orders"])
def get_orders(db: Session = Depends(get_db)):
    return controllers.get_all_orders(db)

@app.get("/orders/{id}", response_model=schemas.Order, tags=["orders"])
def get_order(id: int, db: Session = Depends(get_db)):
    return controllers.get_order_by_id(db, id)

@app.get("/order-products/", response_model=List[schemas.OrderProduct], tags=["order-products"])
def get_order_products(db: Session = Depends(get_db)):
    return controllers.get_all_order_products(db)

@app.get("/order-products/{id}", response_model=schemas.OrderProduct, tags=["order-products"])
def get_order_product(id: int, db: Session = Depends(get_db)):
    return controllers.get_order_product_by_id(db, id)