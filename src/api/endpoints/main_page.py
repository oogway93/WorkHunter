from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Main Page"])


@router.get("/")
async def main_page():
    return JSONResponse(content={"Hello": "My friend!"})
