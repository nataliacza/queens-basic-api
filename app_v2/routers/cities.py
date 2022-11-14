from typing import List

from fastapi import APIRouter

from schemas import City, CitySave

router = APIRouter(prefix="/api/v2/cities",
                   tags=["Cities"])

# region Cities
@router.get("/",
            status_code=200,
            response_model=List[City])
async def get_all_cities():
    result = [{"name": "city",
               "region": "region",
               "country": "country"}]
    return result

# endregion
