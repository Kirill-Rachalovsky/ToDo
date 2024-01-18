from datetime import datetime, timezone

today = datetime.now(timezone.utc).strftime('%d-%m-%Y')


kafka_create_user_message = {
    'action': 'create_user',
    'user_id': 1,
    'email': 'user@gmail.com',
    'username': 'user'
}

kafka_create_task_message = {
    'action': 'create_task',
    'user_id': 1,
    'task_id': 1,
    'task_status': "NOT_STARTED",
    'date_create': "15-01-2024",
}

kafka_update_task_message = {
    "action": "update_task",
    'user_id': 1,
    'task_id': 1,
    'task_status': "DONE",
    'date_create': "15-01-2024",
}

kafka_delete_task_message = {
    "action": "delete_task",
    'user_id': 1,
    'task_id': 1,
}


