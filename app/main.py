from typing import List
from fastapi import FastAPI, HTTPException, Depends

app = FastAPI(
    title="Paye ton kawa",
    description="Le café c'est la vie",
    summary="API Produits",
    version="0.0.2",
)

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