from fastapi import APIRouter, Request
from jose import jwt
from statistic.statistic_params import *

statistic_router = APIRouter()


def get_current_user_id(request: Request):
    token = request.cookies.get('fastapiusersauth')
    claims = jwt.get_unverified_claims(token)
    user_id = claims['sub']
    return int(user_id)


@statistic_router.get('/user_info')
def get_statistic(request: Request):
    cur_user = request.app.mongo_db.find_one({'_id': get_current_user_id(request)})
    return cur_user


@statistic_router.get('/activity')
def get_task_amount(request: Request):
    user_dict = request.app.mongo_db.find_one({'_id': get_current_user_id(request)})
    return activity(user_dict)


@statistic_router.get('/day_activity')
def activity_for_the_day(request: Request):
    user_dict = request.app.mongo_db.find_one({'_id': get_current_user_id(request)})
    return activity(user_dict, 1)


@statistic_router.get('/week_activity')
def activity_for_the_week(request: Request):
    user_dict = request.app.mongo_db.find_one({'_id': get_current_user_id(request)})
    return activity(user_dict, 7)
