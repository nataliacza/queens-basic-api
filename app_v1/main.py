from typing import List
from uuid import UUID

from fastapi import FastAPI
from starlette.responses import JSONResponse

from db_memory import queen_db, city_db, category_db
from helpers import (is_unique_name, is_assigned, update_city_in_queens_db, delete_tag_from_queens_db,
                     update_tag_name_in_queens_db, able_to_add_to_db)
from schemas import Queen, QueenSave, City, CitySave, Category, CategorySave, QueenBase

app = FastAPI(title="Drag Queens Collection API - Beta",
              description="This is a Drag Queens Collection API documentation based on the OpenApi specification.\
              Main goal of the project is to create simple database available for everybody.",
              version="1.0")

# region Queens
@app.get("/api/v1/queens/",
         tags=["Queens"],
         status_code=200,
         response_model=List[QueenBase])
async def get_all_queens():
    result = [queen for queen in queen_db.values()]
    return result


@app.get("/api/v1/queens/{queen_id}",
         tags=["Queens"],
         status_code=200,
         responses={"404": {"code": "404", "message": "Not Found"}},
         response_model=Queen)
async def get_queen(queen_id: UUID):
    result = queen_db.get(queen_id)
    if result:
        return result
    return JSONResponse(status_code=404, content={"code": "404",
                                                  "message": "Not Found"})


@app.post("/api/v1/queens/",
          tags=["Queens"],
          status_code=201,
          responses={"404": {"code": "404", "message": "Not Found"}},
          response_model=Queen)
async def add_queen(queen_details: QueenSave):
    hometown = None
    residence = None
    tags = []
    error = {"status": False, "reason": ""}

    while error["status"] is False:
        if queen_details.hometown is not None:
            get_hometown = city_db.get(queen_details.hometown)
            if get_hometown is None:
                error["status"] = True
                error["reason"] = "Hometown City"
                break
            else:
                hometown = get_hometown

        if queen_details.residence is not None:
            get_residence = city_db.get(queen_details.residence)
            if get_residence is None:
                error["status"] = True
                error["reason"] = "Residence City"
                break
            else:
                residence = get_residence

        if len(queen_details.tags) > 0:
            for tag_id in queen_details.tags:
                get_tag = category_db.get(tag_id)
                if get_tag is None:
                    error["status"] = True
                    error["reason"] = "Tag"
                    break
                else:
                    tags.append(get_tag)
        break

    if error["status"] is True:
        return JSONResponse(status_code=404, content={"code": "404",
                                                      "message": f"{error['reason']} Id Not Found"})

    if not able_to_add_to_db(queen_db):
        return JSONResponse(status_code=400,
                            content={"code": "400", "message": "Number of items in db was exceeded"})

    new_object = Queen(nickname=queen_details.nickname,
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

    queen_db[new_object.queen_id] = new_object.dict()

    return new_object


@app.put("/api/v1/queens/{queen_id}",
         tags=["Queens"],
         status_code=200,
         responses={"404": {"code": "404", "message": "Not Found"}},
         response_model=Queen)
async def update_queen(queen_id: UUID, queen_details: QueenSave):
    find_queen = queen_db.get(queen_id)
    hometown = None
    residence = None
    tags = []
    error = {"status": False, "reason": ""}

    while error["status"] is False:
        if not find_queen:
            error["status"] = True
            error["reason"] = "Queen"
            break

        if queen_details.hometown is not None:
            get_hometown = city_db.get(queen_details.hometown)
            if get_hometown is None:
                error["status"] = True
                error["reason"] = "Hometown City"
                break
            else:
                hometown = get_hometown

        if queen_details.residence is not None:
            get_residence = city_db.get(queen_details.residence)
            if get_residence is None:
                error["status"] = True
                error["reason"] = "Residence City"
                break
            else:
                residence = get_residence

        if len(queen_details.tags) > 0:
            for tag_id in queen_details.tags:
                get_tag = category_db.get(tag_id)
                if get_tag is None:
                    error["status"] = True
                    error["reason"] = "Tag"
                    break
                else:
                    tags.append(get_tag)
        break

    if error["status"] is True:
        return JSONResponse(status_code=404, content={"code": "404",
                                                      "message": f"{error['reason']} Id Not Found"})

    find_queen.update(queen_details.dict())
    find_queen["nickname"] = queen_details.nickname

    if hometown is not None:
        find_queen["hometown"] = hometown

    if residence is not None:
        find_queen["residence"] = residence

    if len(tags) > 0:
        find_queen["tags"] = tags

    queen_db[queen_id] = find_queen

    return find_queen


@app.delete("/api/v1/queens/{queen_id}",
            tags=["Queens"],
            status_code=204,
            responses={"404": {"code": "404", "message": "Not Found"}})
async def delete_queen(queen_id: UUID):
    find_queen = queen_db.get(queen_id)
    if find_queen:
        del queen_db[queen_id]
        return {}

    return JSONResponse(status_code=404, content={"code": "404",
                                                  "message": "Not Found"})
# endregion

# region Cities
@app.get("/api/v1/cities/",
         tags=["Cities"],
         status_code=200,
         response_model=List[City])
async def get_all_cities():
    result = [city for city in city_db.values()]
    return result


@app.get("/api/v1/cities/{city_id}",
         tags=["Cities"],
         status_code=200,
         responses={"404": {"code": "404", "message": "Not Found"}},
         response_model=City)
async def get_city(city_id: UUID):
    result = city_db.get(city_id)
    if result:
        return result
    return JSONResponse(status_code=404, content={"code": "404", "message": "Not Found"})


@app.post("/api/v1/cities/",
          tags=["Cities"],
          status_code=201,
          responses={"400": {"code": "400", "message": "Bad Request"}},
          response_model=City)
async def add_city(city_details: CitySave):
    check = is_unique_name(search=city_details.name.title().strip(),
                           db=city_db)

    if not check:
        return JSONResponse(status_code=400, content={"code": "400",
                                                      "message": "Name must be unique"})

    if not able_to_add_to_db(city_db):
        return JSONResponse(status_code=400,
                            content={"code": "400", "message": "Number of items in db was exceeded"})

    new_object = City(name=city_details.name.title().strip(),
                      region=city_details.region.title().strip(),
                      country=city_details.country.title().strip())

    city_db[new_object.city_id] = new_object.dict()

    return new_object


@app.delete("/api/v1/cities/{city_id}",
            tags=["Cities"],
            description="Unable to delete resource, if any Queen is assigned to city.",
            status_code=204,
            responses={"404": {"code": "404", "message": "Not Found"},
                       "409": {"code": "409", "message": "Conflict"}})
async def delete_city(city_id: UUID):
    """ Deletes city from db with. If city is assigned to queen hometown or residence, it will return 409 code. """
    find_city = city_db.get(city_id)
    if find_city:
        check = is_assigned(search_id=find_city["city_id"])
        if check:
            return JSONResponse(status_code=409, content={"code": "409",
                                                          "message": "City is assigned to queen"})
        del city_db[city_id]
        return {}

    return JSONResponse(status_code=404, content={"code": "404",
                                                  "message": "Not Found"})


@app.put("/api/v1/cities/{city_id}",
         tags=["Cities"],
         status_code=200,
         responses={"400": {"code": "400", "message": "Bad Request"},
                    "404": {"code": "404", "message": "Not Found"}},
         response_model=City)
async def update_city(city_id: UUID, update_data: CitySave):
    """ Updates city in db along with update in queen db if assigned. """
    find_city = city_db.get(city_id)
    if find_city:
        clean_name = update_data.name.title().strip()

        check = is_unique_name(search=clean_name, db=city_db,
                               given_id=city_id, pk_name="city_id")
        if not check:
            return JSONResponse(status_code=400, content={"code": "400",
                                                          "message": "Name must be unique"})
        clean_region = update_data.region.title().strip()
        clean_country = update_data.country.title().strip()

        new_data_cleaned = {"name": clean_name,
                            "region": clean_region,
                            "country": clean_country}

        find_city.update(new_data_cleaned)

        update_city_in_queens_db(city_id, new_data_cleaned)
        return find_city

    return JSONResponse(status_code=404, content={"code": "404",
                                                  "message": "Not Found"})
# endregion

# region Categories
@app.get("/api/v1/categories/",
         tags=["Categories"],
         status_code=200,
         response_model=List[Category])
async def get_all_categories():
    result = [category for category in category_db.values()]
    return result


@app.get("/api/v1/categories/{category_id}",
         tags=["Categories"],
         status_code=200,
         responses={"404": {"code": "404", "message": "Not Found"}},
         response_model=Category)
async def get_category(category_id: UUID):
    result = category_db.get(category_id)
    if result:
        return result
    return JSONResponse(status_code=404, content={"code": "404", "message": "Not Found"})


@app.post("/api/v1/categories/",
          tags=["Categories"],
          status_code=201,
          responses={"400": {"code": "400", "message": "Bad Request"}},
          response_model=Category)
async def add_category(category_details: CategorySave):

    check = is_unique_name(search=category_details.name.lower().strip(),
                           db=category_db)
    if not check:
        return JSONResponse(status_code=400,
                            content={"code": "400", "message": "Name must be unique"})

    if not able_to_add_to_db(category_db):
        return JSONResponse(status_code=400,
                            content={"code": "400", "message": "Number of items in db was exceeded"})

    new_object = Category(name=category_details.name.lower().strip())

    category_db[new_object.category_id] = new_object.dict()

    return new_object


@app.delete("/api/v1/categories/{category_id}",
            tags=["Categories"],
            status_code=204,
            responses={"404": {"code": "404", "message": "Not Found"}})
async def delete_category(category_id: UUID):
    """ Deletes category from db along with deletion in queen db (cascade) if assigned. """
    find_category = category_db.get(category_id)
    if find_category:
        del category_db[category_id]
        delete_tag_from_queens_db(category_id)
        return {}

    return JSONResponse(status_code=404, content={"code": "404",
                                                  "message": "Not Found"})


@app.put("/api/v1/categories/{category_id}",
         tags=["Categories"],
         status_code=200,
         responses={"400": {"code": "400", "message": "Bad Request"},
                    "404": {"code": "404", "message": "Not Found"}},
         response_model=Category)
async def update_category(category_id: UUID, update_data: CategorySave):
    """ Updates category in db along with update in queen db if assigned. """
    find_category = category_db.get(category_id)
    if find_category:
        check = is_unique_name(search=update_data.name.lower().strip(), db=category_db)
        if not check:
            return JSONResponse(status_code=400, content={"code": "400",
                                                          "message": "Name must be unique"})

        clean_name = update_data.name.lower().strip()
        find_category["name"] = clean_name

        update_tag_name_in_queens_db(category_id, clean_name)
        return find_category

    return JSONResponse(status_code=404, content={"code": "404",
                                                  "message": "Not Found"})
# endregion
