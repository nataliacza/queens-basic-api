from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from auth import auth_handler
from config import settings
from database import users_db
from schemas import User, UserBase, AccessToken, UserSave, UserLogin

router = APIRouter(prefix="/api/v2/users",
                   tags=["Users"])


# region Users
@router.post("/signup",
             status_code=200,
             responses={"400": {"code": "400", "message": "Bad Request"},
                        "401": {"code": "401", "message": "Unauthorized"}},
             response_model=User)
async def signup(user_details: UserBase):
    user = users_db.fetch({"username": user_details.username})
    if user.count > 0:
        return JSONResponse(status_code=400, content={"code": "400",
                                                      "message": "Account already exist"})
    try:
        hashed_password = auth_handler.encode_password(user_details.password)
        user = UserSave(username=user_details.username,
                        password=hashed_password)
        save_user = users_db.put(jsonable_encoder(user), expire_at=settings.db_item_expire_at)
        return save_user
    except Exception as e:
        return JSONResponse(status_code=400, content={"code": "400",
                                                      "message": f"Something went wrong: {e}"})


@router.post("/login",
             status_code=200,
             responses={"401": {"code": "401", "message": "Unauthorized"}},
             response_model=AccessToken)
async def login(user_details: UserLogin):
    user = users_db.fetch({"username": user_details.username})

    try:
        if user.count == 1:
            user_dict = user.items[0]
            check_pw = auth_handler.verify_password(user_details.password, user_dict.get("password"))
            if check_pw:
                access_token = auth_handler.encode_token(user_dict.get("username"))
                token_obj = AccessToken(token=access_token)
                return token_obj

        return JSONResponse(status_code=401, content={"code": "401",
                                                      "message": "Invalid username or password"})
    except Exception as e:
        raise Exception(e)

# endregion
