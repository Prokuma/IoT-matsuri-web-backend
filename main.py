from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import router

app = FastAPI(
    title="IoT-matsuri-web-backend"
)

origins = [
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(router,prefix='/api/v1')