from typing import List

from fastapi import APIRouter

from schemas import Category, CategorySave

router = APIRouter(prefix="/api/v2/categories",
                   tags=["Categories"])

# region Categories
@router.get("/",
            status_code=200,
            response_model=List[Category])
async def get_all_categories():
    result = [{"name": "category"}]
    return result

# endregion
