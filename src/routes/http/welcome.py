from fastapi import APIRouter

router = APIRouter(tags=["welcome"])


@router.get("/")
async def root():
    return {"message": "Hello from Portabase Agent !"}
