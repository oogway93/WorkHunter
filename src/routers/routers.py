from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def main_page():
    return {"Hello": "My friend!"}
