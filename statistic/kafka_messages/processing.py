from datetime import datetime, timezone
from fastapi import Request, FastAPI


def task_serializer(instance):
    data_complete = None
    if instance['task_status'] == 'DONE':
        data_complete = datetime.now(timezone.utc).strftime('%d-%m-%Y')

    return {
            "task_id": instance['task_id'],
            "task_status": instance['task_status'],
            "data_create": instance['date_create'],
            "date_complete": data_complete,
        }


def user_serializer(instance):
    return {
        '_id': instance['user_id'],
        'username': instance['username'],
        'email': instance['email'],
        'tasks': [],
        'amount_deleted_tasks': 0
    }


def create_user_event(app: FastAPI(), message):
    app.mongo_db.insert_one(user_serializer(message))
    return {'message': "User created successfully"}


def create_task_event(app: FastAPI(), message):
    app.mongo_db.update_one(
        {'_id': message['user_id']},
        {'$push': {'tasks': task_serializer(message)}}
    )
    return {'message': "Task created successfully"}


def update_task_event(app: FastAPI(), message):
    app.mongo_db.update_one(
        {'_id': message['user_id'], 'tasks.task_id': message['task_id']},
        {'$set': {'tasks.$': task_serializer(message)}}
    )
    return {'message': "Task updated successfully"}


def delete_task_event(app: FastAPI(), message):
    app.mongo_db.update_one({'_id': message['user_id']}, {'$pull': {'tasks': {'task_id': message['task_id']}}})
    app.mongo_db.update_one({'_id': message['user_id']}, {'$inc': {'amount_deleted_tasks': 1}})
    return {'message': 'Task deleted successfully'}


def process_message(app: FastAPI(), kafka_message):
    switch = {
        'create_user': create_user_event,
        'create_task': create_task_event,
        'update_task': update_task_event,
        'delete_task': delete_task_event,
    }

    return switch[kafka_message['action']](app, kafka_message)

