from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List 
from . import controllers, schemas
from .database import get_db
import threading
from .messaging.listener import start_order_service_listener
from .messaging.publisher import send_rabbitmq_message

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

@app.get("/orders/{id}/products", response_model=List[schemas.OrderProduct], tags=["orders"])
def get_order_products(id: int, db: Session = Depends(get_db)):
    return controllers.get_order_products(db, id)

@app.get("/order-products/", response_model=List[schemas.OrderProduct], tags=["order-products"])
def get_order_products(db: Session = Depends(get_db)):
    return controllers.get_all_order_products(db)

@app.get("/order-products/{id}", response_model=schemas.OrderProduct, tags=["order-products"])
def get_order_product(id: int, db: Session = Depends(get_db)):
    return controllers.get_order_product_by_id(db, id)

@app.post("/orders/", response_model=schemas.Order, tags=["orders"])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return controllers.create_order(db, order)

@app.post("/order-products/", response_model=schemas.OrderProduct, tags=["order-products"])
def create_order_product(order_product: schemas.OrderProductCreate, db: Session = Depends(get_db)):
    return controllers.create_order_product(db, order_product)

@app.patch("/orders/{id}", response_model=schemas.Order, tags=["orders"])
def update_order(id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    return controllers.update_order(db, id, order)

@app.patch("/order-products/{id}", response_model=schemas.OrderProduct, tags=["order-products"])
def update_order_product(id: int, order_product: schemas.OrderProductUpdate, db: Session = Depends(get_db)):
    return controllers.update_order_product(db, id, order_product)

@app.delete("/orders/{id}", tags=["orders"])
def delete_order(id: int, db: Session = Depends(get_db)):
    controllers.delete_order(db, id)
    return {"detail": "Order deleted"}

@app.delete("/order-products/{id}", tags=["order-products"])
def delete_order_product(id: int, db: Session = Depends(get_db)):
    controllers.delete_order_product(db, id)
    return {"detail": "OrderProduct deleted"}

@app.get("/orders/{order_id}/products-details", tags=["order-products"])
async def get_order_products_details(order_id: int, db: Session = Depends(get_db)):
    order_products = controllers.get_order_products(db, order_id)
    
    product_ids = [op.productId for op in order_products]

    # Request product details from the Product Service via RabbitMQ
    product_details = send_rabbitmq_message('product_details_queue', {"product_ids": product_ids})
    print(product_details)
    
    return {"order_id": order_id, "products": product_details}

# Start RabbitMQ listener in a separate thread
listener_thread = threading.Thread(target=start_order_service_listener)
listener_thread.start()