from fastapi import APIRouter, Request
from jose import jwt

statistic_router = APIRouter()


@statistic_router.get("/current_user")
def get_current_user_id(request: Request):
    token = request.cookies.get('fastapiusersauth')
    claims = jwt.get_unverified_claims(token)
    user_id = claims['sub']
    return int(user_id)


@statistic_router.get('/info')
def get_statistic(request: Request):
    cur_inst = request.app.mongo_db.find_one({'_id': get_current_user_id(request)})
    return cur_inst
