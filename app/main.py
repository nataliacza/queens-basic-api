from typing import List
from uuid import UUID

import uvicorn
from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.db_memory import category_db, city_db, queen_db
from app.schemas import City, CitySave, Category, CategorySave, Queen, QueenSave


app = FastAPI(title="Drag Queens Base API")


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

# endregion


# Code for debugging
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
