from typing import List
from fastapi import FastAPI, HTTPException, Depends

app = FastAPI(
    title="Paye ton kawa",
    description="Le café c'est la vie",
    summary="API Commandes",
    version="0.0.2",
)
