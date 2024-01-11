import dotenv
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.cors import CORSMiddleware
from jose import jwt

stat_app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
]

stat_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@stat_app.middleware("http")
async def auth_check_middleware(request: Request, call_next):
    token = request.cookies.get('fastapiusersauth')
    if not token:
        raise HTTPException(status_code=401, detail='Not authenticated')
    response = await call_next(request)
    return response


@stat_app.get("/stat")
async def get_stat():
    return {"status": "ok"}


@stat_app.get("/current_user")
async def get_current_user_id(request: Request):
    token = request.cookies.get('fastapiusersauth')
    claims = jwt.get_unverified_claims(token)
    user_id = claims['sub']
    return {'current_user': user_id}
