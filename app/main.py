from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List 
from . import controllers, schemas
from .database import get_db
import threading
from .messaging.listener import start_order_service_listener
from .messaging.publisher import send_rabbitmq_message
from .middleware import get_current_user, is_admin, is_customer_or_admin

app = FastAPI(
    title="Paye ton kawa",
    description="Le café c'est la vie",
    summary="API Commandes",
    version="0.0.2",
)

# Start RabbitMQ listener in a separate thread
listener_thread = threading.Thread(target=start_order_service_listener)
listener_thread.start()

# ---------------------- Orders Endpoints ---------------------- #

@app.get("/orders/", response_model=List[schemas.Order], tags=["orders"])
async def get_orders(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Retrieve all orders if the user is an admin.
    """
    try:
        is_admin(current_user)
        orders = controllers.get_all_orders(db)

        if not orders:
            raise HTTPException(status_code=404, detail="No orders found")
        return orders

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error retrieving orders: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving orders")


@app.get("/orders/{id}", response_model=schemas.Order, tags=["orders"])
async def get_customer_orders(id: int, db: Session = Depends(get_db), current_customer: dict = Depends(get_current_user)):
    """
    Retrieve orders for a specific customer. Accessible to the customer or admin.
    """
    try:
        order = controllers.get_order_by_id(db, id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        is_customer_or_admin(current_customer, order.customerId)
        return order

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error retrieving order with id {id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the order")


@app.get("/orders/{id}/products", response_model=List[schemas.OrderProduct], tags=["orders"])
async def get_order_products(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Retrieve the products for a specific order. Accessible to the customer or admin.
    """
    try:
        order = controllers.get_order_by_id(db, id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        is_customer_or_admin(current_user, order.customerId)
        return order.order_products

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error retrieving products for order with id {id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving order products")


@app.post("/orders/", response_model=schemas.Order, tags=["orders"])
async def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Create a new order. Accessible to the customer or admin.
    """
    try:
        is_customer_or_admin(current_user, order.customerId)
        new_order = controllers.create_order(db, order)
        return new_order

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error creating order for customer with id {order.customer_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the order")


@app.patch("/orders/{id}", response_model=schemas.Order, tags=["orders"])
async def update_order(id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Update an order. Accessible to the customer or admin.
    """
    try:
        order_data = controllers.get_order_by_id(db, id)
        if not order_data:
            raise HTTPException(status_code=404, detail=f"Order with id {id} not found")

        is_customer_or_admin(current_user, order_data.customerId)
        updated_order = controllers.update_order(db, id, order)
        return updated_order

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error updating order with id {id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the order")


@app.delete("/orders/{id}", tags=["orders"])
async def delete_order(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Delete an order. Accessible to the customer or admin.
    """
    try:
        order_data = controllers.get_order_by_id(db, id)
    
        if not order_data:
            raise HTTPException(status_code=404, detail=f"Order with id {id} not found")
        
        is_customer_or_admin(current_user, order_data.customerId)
        controllers.delete_order(db, id)
        return {"detail": f"Order with id {id} deleted successfully"}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error deleting order with id {id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while deleting the order")


# ---------------------- Order Products Endpoints ---------------------- #

@app.get("/order-products/", response_model=List[schemas.OrderProduct], tags=["order-products"])
async def get_all_order_products(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Retrieve all order products. Only accessible to admin.
    """
    try:
        is_admin(current_user)
        order_products = controllers.get_all_order_products(db)

        if not order_products:
            raise HTTPException(status_code=404, detail="No order products found")

        return order_products

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error fetching order products: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the order products")


@app.get("/order-products/{id}", response_model=schemas.OrderProduct, tags=["order-products"])
async def get_order_product(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Retrieve a specific order product. Accessible to the customer or admin.
    """
    try:
        order_product = controllers.get_order_product_by_id(db, id)
        if not order_product:
            raise HTTPException(status_code=404, detail="OrderProduct not found")
        
        order = controllers.get_order_by_id(db, order_product.id_order)

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        is_customer_or_admin(current_user, order.customerId)
        return order_product
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error retrieving order product with id {id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the order product")


@app.post("/order-products/", response_model=schemas.OrderProduct, tags=["order-products"])
async def create_order_product(order_product: schemas.OrderProductCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):    
    try:
        is_customer_or_admin(current_user, current_user["id_customer"]) 
        new_order_product = controllers.create_order_product(db, order_product)
        return new_order_product
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error creating order product for order with id {order_product.order_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the order product")


@app.patch("/order-products/{id}", response_model=schemas.OrderProduct, tags=["order-products"])
async def update_order_product(id: int, order_product_data: schemas.OrderProductUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Update an order product. Accessible to the customer or admin.
    """
    try:
        order_product = controllers.get_order_product_by_id(db, id)
        if not order_product:
            raise HTTPException(status_code=404, detail="OrderProduct not found")

        order = controllers.get_order_by_id(db, order_product.id_order)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        is_customer_or_admin(current_user, order.customerId)
        updated_order_product = controllers.update_order_product(db, id, order_product_data)
        return updated_order_product

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error updating order product with id {id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the order product")


@app.delete("/order-products/{id}", tags=["order-products"])
async def delete_order_product(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Delete an order product. Accessible to the customer or admin.
    """
    try:
        order_product = controllers.get_order_product_by_id(db, id)
        if not order_product:
            raise HTTPException(status_code=404, detail="OrderProduct not found")

        order = controllers.get_order_by_id(db, order_product.id_order)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        is_customer_or_admin(current_user, order.customerId)
        controllers.delete_order_product(db, id)
        return {"detail": "OrderProduct deleted successfully"}

    except HTTPException as http_exc:
        raise http_exc
    except ValueError as ve:
        print(f"ValueError: {ve}")
        raise HTTPException(status_code=400, detail="Invalid input data")
    except KeyError as ke:
        print(f"KeyError: {ke}")
        raise HTTPException(status_code=400, detail=f"Missing or invalid data: {ke}")
    except Exception as e:
        print(f"Error deleting order product with id {id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while deleting the order product")

# ---------------------- Order Products Details ---------------------- #

@app.get("/orders/{order_id}/products-details", tags=["order-products"])
async def get_order_products_details(order_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Retrieve product details for an order. Accessible to the customer who owns the order or an admin.
    """
    order = controllers.get_order_by_id(db, order_id)
    is_customer_or_admin(current_user, order.id_order)

    order_products = controllers.get_order_products(db, order_id)
    product_ids = [op.productId for op in order_products]
    product_details = send_rabbitmq_message('product_details_queue', {"product_ids": product_ids})
    print(product_details)
    
    return {"order_id": order_id, "products": product_details}