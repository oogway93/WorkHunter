from fastapi import APIRouter
from endpoints import main_page
from endpoints import worker


api_router = APIRouter()

api_router.include_router(main_page.router)
api_router.include_router(worker.router)
