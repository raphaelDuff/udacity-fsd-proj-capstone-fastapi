from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from routers.movies import router as movies_router


app = FastAPI()  # FastAPI(lifespan=lifespan)

app.include_router(movies_router)
