from typing import List

import uvicorn
from fastapi import FastAPI

from db_memory import queen_db
from schemas import Queen

app = FastAPI(title="Drag Queens Base API")


@app.get("/v1/queens/",
         tags=["Queens"],
         status_code=200,
         response_model=List[Queen])
async def get_all_queens():
    result = [queen for queen in queen_db.values()]
    return result


# Code for debugging
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
