from fastapi import APIRouter, Depends
from pydantic import BaseModel

router = APIRouter(prefix="/server/v1/")


class CreateUserRequest(BaseModel):
    login: str
    password: str


class CreateUserResponse(BaseModel):
    access_token: str


# users
# id PK (autoincrement)
# access_token string
# expires_at Datetime (2 hours)
# created_at Datetime
# login string
# password string (sha encoded)

# disks
# id
# user_id FK
# volume
#
@router.post(
    "/create_user")
async def add_user_to_db(request: CreateUserRequest) -> CreateUserResponse:
    return await BuyItemHandler.handle(request)


@router.get("/all_users")
async def get_all_users():
    sql = "SELECT * FROM users;"
    pass


@router.get("/all_connected_users")
async def get_all_users():
    sql = "Select * from users where acess_token > datetime.now()"


@router.get("/all_authorized_users")
async def get_all_auth_users():
    pass


@router.get("/get_disks")
async def get_all_disks():
    pass