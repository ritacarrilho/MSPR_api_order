"""
Module with all the API endpoints for orders management.
It includes the operations of creation, lecture, update and delete of orders
"""

from typing import List
from fastapi import FastAPI, HTTPException, Depends


app = FastAPI()

@app.get("/", response_model=dict, tags=["Health Check"])
def api_status():
    """
    Verifies the API status.

    Returns:
        dict: dict with the API status.
    """
    return {"status": "running"}



@app.get("/orders/", tags=["Orders"])
def get_orders():
    return {"get orders": "ok"}


@app.get("/orders/{id}", tags=["Orders"])
def get_order():
    return {"get order by id": "ok"}