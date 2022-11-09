from typing import List
from uuid import UUID

import uvicorn
from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.db_memory import category_db, city_db, queen_db
from app.helpers import (is_unique, is_assigned, generate_new_uuid,
                         delete_tag_from_queens_db, update_tag_name_in_queens_db,
                         update_city_in_queens_db)
from app.schemas import (City, CitySave, Category, CategorySave, Queen, QueenSave)


app = FastAPI(title="Drag Queens Basic API")


# region Queens

@app.get("/v1/queens/",
         tags=["Queens"],
         status_code=200,
         response_model=List[Queen])
async def get_all_queens():
    result = [queen for queen in queen_db.values()]
    return result


@app.get("/v1/queens/{queen_id}",
         tags=["Queens"],
         status_code=200,
         responses={"404": {"code": "404", "message": "Not Found"}},
         response_model=Queen)
async def get_queen(queen_id: UUID):
    result = queen_db.get(str(queen_id))
    if result:
        return result
    return JSONResponse(status_code=404, content={"code": "404",
                                                  "message": "Not Found"})


@app.post("/v1/queens/",
          tags=["Queens"],
          status_code=201,
          responses={"404": {"code": "404", "message": "Not Found"}},
          response_model=Queen)
async def add_queen(queen_details: QueenSave):

    hometown = None
    residence = None
    tags = []

    # TODO: refactor those to separate functions - used probably also in update
    if queen_details.hometown_id is not None:
        get_hometown = city_db.get(str(queen_details.hometown_id))
        if get_hometown is None:
            return JSONResponse(status_code=404, content={"code": "404",
                                                          "message": "Hometown City Id Not Found"})
        hometown = get_hometown

    if queen_details.residence_id is not None:
        get_residence = city_db.get(str(queen_details.residence_id))
        if get_residence is None:
            return JSONResponse(status_code=404, content={"code": "404",
                                                          "message": "Residence City Id Not Found"})
        residence = get_residence

    if queen_details.tag_ids is not None:
        for tag_id in queen_details.tag_ids:
            get_tag = category_db.get(str(tag_id))
            if get_tag is None:
                return JSONResponse(status_code=404, content={"code": "404",
                                                              "message": "Tag Id Not Found"})
            tags.append(get_tag)

    new_object = Queen(queen_id=generate_new_uuid(),
                       nickname=queen_details.nickname,
                       status=queen_details.status,
                       info=queen_details.info,
                       on_stage_since=queen_details.on_stage_since,
                       hometown=hometown,
                       residence=residence,
                       email=queen_details.email,
                       web=queen_details.web,
                       instagram=queen_details.instagram,
                       facebook=queen_details.facebook,
                       twitter=queen_details.twitter,
                       tags=tags)

    queen_db[str(new_object.queen_id)] = new_object.dict()

    return new_object


@app.delete("/v1/queens/{queen_id}",
            tags=["Queens"],
            status_code=204,
            responses={"404": {"code": "404", "message": "Not Found"}})
async def delete_queen(queen_id: UUID):
    find_queen = queen_db.get(str(queen_id))
    if find_queen:
        del queen_db[str(queen_id)]
        return {}

    return JSONResponse(status_code=404, content={"code": "404",
                                                  "message": "Not Found"})

# endregion

# region Cities

@app.get("/v1/cities/",
         tags=["Cities"],
         status_code=200,
         response_model=List[City])
async def get_all_cities():
    result = [city for city in city_db.values()]
    return result


@app.get("/v1/cities/{city_id}",
         tags=["Cities"],
         status_code=200,
         responses={"404": {"code": "404", "message": "Not Found"}},
         response_model=City)
async def get_city(city_id: UUID):
    result = city_db.get(str(city_id))
    if result:
        return result
    return JSONResponse(status_code=404, content={"code": "404", "message": "Not Found"})


@app.post("/v1/cities/",
          tags=["Cities"],
          status_code=201,
          responses={"400": {"code": "400", "message": "Bad Request"}},
          response_model=City)
async def add_city(city_details: CitySave):

    check = is_unique(search=city_details.name.title().strip(),
                      in_key="name",
                      db=city_db)

    if not check:
        return JSONResponse(status_code=400, content={"code": "400",
                                                      "message": "Name must be unique"})

    new_object = City(city_id=generate_new_uuid(),
                      name=city_details.name.title().strip(),
                      region=city_details.region,
                      country=city_details.country)

    city_db[str(new_object.city_id)] = new_object.dict()

    return new_object


@app.delete("/v1/cities/{city_id}",
            tags=["Cities"],
            status_code=204,
            responses={"404": {"code": "404", "message": "Not Found"},
                       "409": {"code": "409", "message": "Conflict"}})
async def delete_city(city_id: UUID):
    find_city = city_db.get(str(city_id))
    if find_city:
        check = is_assigned(search_id=find_city["city_id"])
        if check:
            return JSONResponse(status_code=409, content={"code": "409",
                                                          "message": "City is assigned to queen"})
        del city_db[str(city_id)]
        return {}

    return JSONResponse(status_code=404, content={"code": "404",
                                                  "message": "Not Found"})


@app.put("/v1/cities/{city_id}",
         tags=["Cities"],
         status_code=200,
         responses={"400": {"code": "400", "message": "Bad Request"},
                    "404": {"code": "404", "message": "Not Found"}},
         response_model=City)
async def update_city(city_id: UUID, update_data: CitySave):
    find_city = city_db.get(str(city_id))
    if find_city:
        clean_name = update_data.name.title().strip()

        check = is_unique(search=clean_name, in_key="name", db=city_db)
        if not check:
            return JSONResponse(status_code=400, content={"code": "400",
                                                          "message": "Name must be unique"})
        clean_region = update_data.region.title().strip()
        clean_country = update_data.country.title().strip()

        new_data_cleaned = {"name": clean_name,
                            "region": clean_region,
                            "country": clean_country}

        find_city.update(new_data_cleaned)

        update_city_in_queens_db(str(city_id), new_data_cleaned)
        return find_city

    return JSONResponse(status_code=404, content={"code": "404",
                                                  "message": "Not Found"})

# endregion

# region Categories

@app.get("/v1/categories/",
         tags=["Categories"],
         status_code=200,
         response_model=List[Category])
async def get_all_categories():
    result = [category for category in category_db.values()]
    return result


@app.get("/v1/categories/{category_id}",
         tags=["Categories"],
         status_code=200,
         responses={"404": {"code": "404", "message": "Not Found"}},
         response_model=Category)
async def get_category(category_id: UUID):
    result = category_db.get(str(category_id))
    if result:
        return result
    return JSONResponse(status_code=404, content={"code": "404", "message": "Not Found"})


@app.post("/v1/categories/",
          tags=["Categories"],
          status_code=201,
          responses={"400": {"code": "400", "message": "Bad Request"}},
          response_model=Category)
async def add_category(category_details: CategorySave):

    check = is_unique(search=category_details.name.lower().strip(),
                      in_key="name",
                      db=category_db)
    if not check:
        return JSONResponse(status_code=400,
                            content={"code": "400", "message": "Name must be unique"})

    new_object = Category(category_id=generate_new_uuid(),
                          name=category_details.name.lower().strip())

    category_db[str(new_object.category_id)] = new_object.dict()

    return new_object


@app.delete("/v1/categories/{category_id}",
            tags=["Categories"],
            status_code=204,
            responses={"404": {"code": "404", "message": "Not Found"}})
async def delete_category(category_id: UUID):
    find_category = category_db.get(str(category_id))
    if find_category:
        del category_db[str(category_id)]
        delete_tag_from_queens_db(str(category_id))
        return {}

    return JSONResponse(status_code=404, content={"code": "404",
                                                  "message": "Not Found"})


@app.put("/v1/categories/{category_id}",
         tags=["Categories"],
         status_code=200,
         responses={"400": {"code": "400", "message": "Bad Request"},
                    "404": {"code": "404", "message": "Not Found"}},
         response_model=Category)
async def update_category(category_id: UUID, update_data: CategorySave):
    find_category = category_db.get(str(category_id))
    if find_category:
        check = is_unique(search=update_data.name.lower().strip(), in_key="name", db=category_db)
        if not check:
            return JSONResponse(status_code=400, content={"code": "400",
                                                          "message": "Name must be unique"})

        clean_name = update_data.name.lower().strip()
        find_category["name"] = clean_name

        update_tag_name_in_queens_db(str(category_id), clean_name)
        return find_category

    return JSONResponse(status_code=404, content={"code": "404",
                                                  "message": "Not Found"})

# endregion


# Code for debugging
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
