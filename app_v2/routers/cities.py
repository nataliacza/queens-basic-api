from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from auth.auth_bearer import JWTBearer
from config import settings
from database import cities_db
from helpers import (is_unique_name, is_assigned, is_unique_name_update, update_city_in_queens_db)
from schemas import City, CitySave

router = APIRouter(prefix="/api/v2/cities",
                   tags=["Cities"])

# region Cities
@router.get("/",
            status_code=200,
            responses={"401": {"code": "401", "message": "Unauthorized"},
                       "403": {"code": "403", "message": "Not Authenticated"}},
            response_model=List[City],
            dependencies=[Depends(JWTBearer())])
async def get_all_cities():
    fetch_db = cities_db.fetch().items
    return fetch_db


@router.get("/{city_id}",
            status_code=200,
            responses={"401": {"code": "401", "message": "Unauthorized"},
                       "403": {"code": "403", "message": "Not Authenticated"},
                       "404": {"code": "404", "message": "Not Found"}},
            response_model=City,
            dependencies=[Depends(JWTBearer())])
async def get_city(city_id: UUID):
    get_item = cities_db.get(jsonable_encoder(city_id))
    if get_item:
        return get_item
    return JSONResponse(status_code=404, content={"code": "404", "message": "Not Found"})


@router.post("/",
             status_code=201,
             responses={"400": {"code": "400", "message": "Bad Request"},
                        "401": {"code": "401", "message": "Unauthorized"},
                        "403": {"code": "403", "message": "Not Authenticated"},
                        "507": {"code": "507", "message": "Insufficient Storage"}},
             response_model=City,
             dependencies=[Depends(JWTBearer())])
async def add_city(city_details: CitySave):
    fetch_db = cities_db.fetch()
    if fetch_db.count == settings.db_limit:
        return JSONResponse(status_code=400,
                            content={"code": "507", "message": "Number of items in db was exceeded"})

    clean_name = city_details.name.title().strip()
    check = is_unique_name(fraze=clean_name, given_data=fetch_db.items)
    if not check:
        return JSONResponse(status_code=400, content={"code": "400",
                                                      "message": "Name must be unique"})

    clean_region = city_details.region.title().strip()
    clean_country = city_details.country.title().strip()
    new_item = City(name=clean_name,
                    region=clean_region,
                    country=clean_country)

    save_item = cities_db.put(jsonable_encoder(new_item), expire_at=settings.db_item_expire_at)
    return save_item


@router.delete("/{city_id}",
               description="Unable to delete resource, if city is assigned to queen.",
               status_code=204,
               responses={"401": {"code": "401", "message": "Unauthorized"},
                          "403": {"code": "403", "message": "Not Authenticated"},
                          "404": {"code": "404", "message": "Not Found"},
                          "409": {"code": "409", "message": "Conflict"}},
               dependencies=[Depends(JWTBearer())])
async def delete_city(city_id: UUID):
    """ Deletes city from db. If city is assigned to queen hometown or residence, it will return 409 code. """
    encoded_id = jsonable_encoder(city_id)
    get_item = cities_db.get(encoded_id)
    if get_item:
        check = is_assigned(search_id=encoded_id)
        if check:
            return JSONResponse(status_code=409, content={"code": "409",
                                                          "message": "City is assigned to queen"})
        cities_db.delete(encoded_id)
        return {}

    return JSONResponse(status_code=404, content={"code": "404",
                                                  "message": "Not Found"})


@router.put("/{city_id}",
            status_code=200,
            responses={"400": {"code": "400", "message": "Bad Request"},
                       "401": {"code": "401", "message": "Unauthorized"},
                       "403": {"code": "403", "message": "Not Authenticated"},
                       "404": {"code": "404", "message": "Not Found"}},
            response_model=City,
            dependencies=[Depends(JWTBearer())])
async def update_city(city_id: UUID, update_data: CitySave):
    """ Updates city in db along with update in queen db if assigned. """
    encoded_id = jsonable_encoder(city_id)
    get_item = cities_db.get(encoded_id)
    if get_item:
        clean_name = update_data.name.title().strip()
        check = is_unique_name_update(fraze=clean_name, given_data=cities_db.fetch().items, update_id=encoded_id)
        if not check:
            return JSONResponse(status_code=400, content={"code": "400",
                                                          "message": "Name must be unique"})
        clean_region = update_data.region.title().strip()
        clean_country = update_data.country.title().strip()

        new_data = {"name": clean_name,
                    "region": clean_region,
                    "country": clean_country}

        save_item = cities_db.put(key=encoded_id,
                                  data=new_data,
                                  expire_at=settings.db_item_expire_at)
        update_city_in_queens_db(encoded_id, new_data)
        return save_item

    return JSONResponse(status_code=404, content={"code": "404",
                                                  "message": "Not Found"})
# endregion
