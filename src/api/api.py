from fastapi import APIRouter
from .endpoints import worker, main

api_router = APIRouter()
api_router.include_router(worker.router)
api_router.include_router(main.router)
