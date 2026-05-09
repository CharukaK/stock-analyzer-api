from fastapi import APIRouter


router = APIRouter()


@router.get("/symbols")
async def symbols():
    return {"symbol/hello"}
