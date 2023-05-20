from fastapi import APIRouter
from starlette.responses import RedirectResponse

router = APIRouter(tags=["Index"])


# region Index
@router.get(path="/", status_code=200, include_in_schema=False)
async def index_redirect():
    response = RedirectResponse(url="/docs")
    return response


# endregion
