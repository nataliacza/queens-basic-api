from typing import List

from fastapi import APIRouter

from schemas import QueenBase

router = APIRouter(prefix="/api/v2/queens",
                   tags=["Queens"])

# region Queens
@router.get("/",
            status_code=200,
            response_model=List[QueenBase])
async def get_all_queens():
    result = [{"nickname": "queen"}]
    return result

# endregion
