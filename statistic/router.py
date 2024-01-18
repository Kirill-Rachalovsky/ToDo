from fastapi import APIRouter, Request
from jose import jwt

statistic_router = APIRouter()


async def get_current_user_id(request: Request):
    token = request.cookies.get('fastapiusersauth')
    claims = jwt.get_unverified_claims(token)
    user_id = claims['sub']
    return user_id
