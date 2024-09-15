from app.routers import songs
from fastapi import FastAPI

api_router = FastAPI()


@api_router.get("/")
async def healthcheck():
    return {"status": "ok"}


api_router.include_router(songs.router, prefix="/songs", tags=["songs"])
