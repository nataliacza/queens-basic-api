from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from config import settings
from database import queens_db, cities_db, categories_db
from schemas import QueenBase, Queen, QueenSave

router = APIRouter(prefix="/api/v2/queens",
                   tags=["Queens"])

# region Queens
@router.get("/",
            status_code=200,
            response_model=List[QueenBase])
async def get_all_queens():
    fetch_db = queens_db.fetch().items
    return fetch_db


@router.get("/{queen_id}",
            status_code=200,
            responses={"404": {"code": "404", "message": "Not Found"}},
            response_model=Queen)
async def get_queen(queen_id: UUID):
    result = queens_db.get(jsonable_encoder(queen_id))
    if result:
        return result
    return JSONResponse(status_code=404, content={"code": "404",
                                                  "message": "Not Found"})


@router.post("/",
             status_code=201,
             responses={"401": {"code": "401", "message": "Unauthorized"},
                        "404": {"code": "404", "message": "Not Found"},
                        "507": {"code": "507", "message": "Insufficient Storage"}},
             response_model=Queen)
async def add_queen(queen_details: QueenSave):
    hometown = None
    residence = None
    tags = []
    error = {"status": False, "reason": ""}

    fetch_db = queens_db.fetch()
    if fetch_db.count == settings.db_limit:
        return JSONResponse(status_code=400,
                            content={"code": "507", "message": "Number of items in db was exceeded"})

    while error["status"] is False:
        if queen_details.hometown is not None:
            get_hometown = cities_db.get(jsonable_encoder(queen_details.hometown))
            if get_hometown is None:
                error["status"] = True
                error["reason"] = "Hometown City"
                break
            hometown = get_hometown

        if queen_details.residence is not None:
            get_residence = cities_db.get(jsonable_encoder(queen_details.residence))
            if get_residence is None:
                error["status"] = True
                error["reason"] = "Residence City"
                break
            residence = get_residence

        if len(queen_details.tags) > 0:
            for tag_key in queen_details.tags:
                get_tag = categories_db.get(jsonable_encoder(tag_key))
                if get_tag is None:
                    error["status"] = True
                    error["reason"] = "Tag"
                    break
                tags.append(get_tag)
        break

    if error["status"] is True:
        return JSONResponse(status_code=404, content={"code": "404",
                                                      "message": f"{error['reason']} Id Not Found"})

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

    save_item = queens_db.put(jsonable_encoder(new_object), expire_at=settings.db_item_expire_at)
    return save_item


@router.delete("/{queen_id}",
               status_code=204,
               responses={"401": {"code": "401", "message": "Unauthorized"},
                          "404": {"code": "404", "message": "Not Found"}})
async def delete_queen(queen_id: UUID):
    encoded_id = jsonable_encoder(queen_id)
    get_item = queens_db.get(encoded_id)
    if get_item:
        queens_db.delete(encoded_id)
        return {}

    return JSONResponse(status_code=404, content={"code": "404",
                                                  "message": "Not Found"})


@router.put("/{queen_id}",
            status_code=200,
            responses={"401": {"code": "401", "message": "Unauthorized"},
                       "404": {"code": "404", "message": "Not Found"}},
            response_model=Queen)
async def update_queen(queen_id: UUID, update_data: QueenSave):
    encoded_id = jsonable_encoder(queen_id)
    find_queen = queens_db.get(encoded_id)
    hometown = None
    residence = None
    tags = []
    error = {"status": False, "reason": ""}

    while error["status"] is False:
        if not find_queen:
            error["status"] = True
            error["reason"] = "Queen"
            break

        if update_data.hometown is not None:
            get_hometown = cities_db.get(jsonable_encoder(update_data.hometown))
            if get_hometown is None:
                error["status"] = True
                error["reason"] = "Hometown City"
                break
            hometown = get_hometown

        if update_data.residence is not None:
            get_residence = cities_db.get(jsonable_encoder(update_data.residence))
            if get_residence is None:
                error["status"] = True
                error["reason"] = "Residence City"
                break
            residence = get_residence

        if len(update_data.tags) > 0:
            for tag_id in update_data.tags:
                get_tag = categories_db.get(jsonable_encoder(tag_id))
                if get_tag is None:
                    error["status"] = True
                    error["reason"] = "Tag"
                    break
                tags.append(get_tag)
        break

    if error["status"] is True:
        return JSONResponse(status_code=404, content={"code": "404",
                                                      "message": f"{error['reason']} Id Not Found"})

    find_queen.update(update_data.dict())

    if hometown is not None:
        find_queen["hometown"] = hometown

    if residence is not None:
        find_queen["residence"] = residence

    if len(tags) > 0:
        find_queen["tags"] = tags

    save_item = queens_db.put(key=encoded_id,
                              data=find_queen,
                              expire_at=settings.db_item_expire_at)
    return save_item

# endregion
