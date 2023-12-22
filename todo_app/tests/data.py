user_payload = {
    "email": "USER",
    "password": "PASS",
    "username": "user",
    "is_active": True,
    "is_superuser": False,
    "is_verified": False
}


board_payload = {
    "title": "My board",
    "tasks": [
        {
            "status": "NOT_STARTED",
            "task_text": "Do homework"
        },
        {
            "status": "NOT_STARTED",
            "task_text": "Make dinner"
        },
        {
            "status": "NOT_STARTED",
            "task_text": "Clean the room"
        }
    ]
}


board_update_payload = {
    "new_title": "My new Board"
}


task_payload = {
    "status": "NOT_STARTED",
    "task_text": "Task text"
}


task_update_payload = {
    "status": "DONE",
    "task_text": "New task text"
}

