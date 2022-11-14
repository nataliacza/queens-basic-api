from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from config import settings
from database import categories_db
from helpers import is_unique_name
from schemas import Category, CategorySave

router = APIRouter(prefix="/api/v2/categories",
                   tags=["Categories"])

# region Categories
@router.get("/",
            status_code=200,
            responses={"401": {"code": "401", "message": "Unauthorized"}},
            response_model=List[Category])
async def get_all_categories():
    fetch_db = categories_db.fetch().items
    return fetch_db


@router.get("/{category_id}",
            status_code=200,
            responses={"401": {"code": "401", "message": "Unauthorized"},
                       "404": {"code": "404", "message": "Not Found"}},
            response_model=Category)
async def get_category(category_id: UUID):
    get_item = categories_db.get(jsonable_encoder(category_id))
    if get_item:
        return get_item
    return JSONResponse(status_code=404, content={"code": "404", "message": "Not Found"})


@router.post("/",
             status_code=201,
             responses={"400": {"code": "400", "message": "Bad Request"},
                        "401": {"code": "401", "message": "Unauthorized"}},
             response_model=Category)
async def add_category(category_details: CategorySave):
    clean_name = category_details.name.lower().strip()
    fetch_db = categories_db.fetch()

    if fetch_db.count == settings.db_limit:
        return JSONResponse(status_code=400,
                            content={"code": "400", "message": "Number of items in db was exceeded"})

    if not is_unique_name(clean_name, fetch_db.items):
        return JSONResponse(status_code=400,
                            content={"code": "400", "message": "Name must be unique"})

    new_item = Category(name=clean_name)
    save_item = categories_db.put(jsonable_encoder(new_item), expire_at=settings.db_item_expire_at)
    return save_item


@router.delete("/{category_id}",
               status_code=204,
               responses={"401": {"code": "401", "message": "Unauthorized"},
                          "404": {"code": "404", "message": "Not Found"}})
async def delete_category(category_id: UUID):
    # TODO: cover extra deletion in queens db
    get_item = categories_db.get(jsonable_encoder(category_id))
    if get_item:
        categories_db.delete(jsonable_encoder(category_id))
        return {}

    return JSONResponse(status_code=404, content={"code": "404",
                                                  "message": "Not Found"})


@router.put("{category_id}",
            status_code=200,
            responses={"400": {"code": "400", "message": "Bad Request"},
                       "401": {"code": "401", "message": "Unauthorized"},
                       "404": {"code": "404", "message": "Not Found"}},
            response_model=Category)
async def update_category(category_id: UUID, update_data: CategorySave):
    # TODO: cover extra update in queens db
    encoded_id = jsonable_encoder(category_id)
    get_item = categories_db.get(encoded_id)
    if get_item:
        clean_name = update_data.name.lower().strip()
        check = is_unique_name(fraze=clean_name, given_data=categories_db.fetch().items)
        if not check:
            return JSONResponse(status_code=400, content={"code": "400",
                                                          "message": "Name must be unique"})

        save_item = categories_db.put(key=encoded_id,
                                      data={"name": clean_name},
                                      expire_at=settings.db_item_expire_at)
        return save_item

    return JSONResponse(status_code=404, content={"code": "404",
                                                  "message": "Not Found"})

# endregion
