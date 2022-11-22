from fastapi import FastAPI

from config import settings
from routers import categories, cities, users, queens, index

app = FastAPI(title=settings.title,
              description=settings.description,
              version=settings.version)


app.include_router(queens.router)
app.include_router(categories.router)
app.include_router(cities.router)
app.include_router(users.router)
app.include_router(index.router)
