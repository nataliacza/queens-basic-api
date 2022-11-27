from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import settings
from routers import categories, cities, users, queens, index

app = FastAPI(title=settings.title,
              description=settings.description,
              version=settings.version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)

app.include_router(queens.router)
app.include_router(categories.router)
app.include_router(cities.router)
app.include_router(users.router)
app.include_router(index.router)
