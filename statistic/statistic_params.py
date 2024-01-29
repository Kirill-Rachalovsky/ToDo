from datetime import datetime, timedelta


def from_str_to_date(string):
    data_format = '%Y-%m-%d'
    return datetime.strptime(string, data_format)


def generate_params(task_list: dict):
    not_started = 0
    tasks_in_progress = 0
    completed_tasks = 0

    for task in task_list:
        if task['task_status'] == "NOT_STARTED":
            not_started +=1
        elif task['task_status'] == "IN_PROGRESS":
            tasks_in_progress += 1
        elif task['task_status'] == "DONE":
            completed_tasks += 1

    return {
        'all_tasks': len(task_list),
        'not_started': not_started,
        'tasks_in_progress': tasks_in_progress,
        'completed_tasks': completed_tasks,
        'deleted_task': task_list['amount_deleted_tasks'],
        'complete_percent': int(100 * completed_tasks / len(task_list))
    }


def activity(user_dict: dict, time_period: int | None = None) -> dict:

    not_started = 0
    tasks_in_progress = 0
    completed_tasks = 0

    task_list = []

    if time_period is None:
        task_list = user_dict['tasks']
    else:
        today = datetime.today()

        for task in user_dict['tasks']:
            task_created = from_str_to_date(task['data_create'])
            if today - task_created < timedelta(days=time_period):
                task_list.append(task)

    for task in task_list:
        if task['task_status'] == "NOT_STARTED":
            not_started +=1
        elif task['task_status'] == "IN_PROGRESS":
            tasks_in_progress += 1
        elif task['task_status'] == "DONE":
            completed_tasks += 1

    return {
        'all_tasks': len(user_dict['tasks']),
        'not_started': not_started,
        'tasks_in_progress': tasks_in_progress,
        'completed_tasks': completed_tasks,
        'deleted_task': user_dict['amount_deleted_tasks'],
        'complete_percent': int(100 * completed_tasks / len(user_dict['tasks']))
    }





