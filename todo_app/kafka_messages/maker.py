from datetime import datetime, timezone

today = datetime.now(timezone.utc).strftime('%d-%m-%Y')


def create_user_message(user_instance):
    return {
        'action': 'create_user',
        'user_id': user_instance.id,
        'email': user_instance.email,
        'username': user_instance.username
    }


def create_task_message(user_id, task_instance):
    return {
        'action': 'create_task',
        'user_id': user_id,
        'task_id': task_instance.id,
        'task_status': task_instance.status,
        'date_created': task_instance.date_created
    }


def update_task_message(user_id, task_instance):
    return {
        'action': 'update_task',
        'user_id': user_id,
        'task_id': task_instance.id,
        'task_status': task_instance.status,
        'date_created': task_instance.date_created
    }


def delete_task_message(user_id, task_id):
    return {
        'action': 'delete_task',
        'user_id': user_id,
        'task_id': task_id,
    }
