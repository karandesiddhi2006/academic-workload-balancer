from datetime import date, datetime, time

from app.models import Task


def get_upcoming_tasks(user_id, limit=None):
    """Return pending tasks with deadlines today or in the future."""
    today = date.today()

    query = (
        Task.query
        .filter(
            Task.user_id == user_id,
            Task.status == "PENDING",
            Task.due_date >= today
        )
        .order_by(Task.due_date.asc(), Task.due_time.asc())
    )

    if limit:
        query = query.limit(limit)

    return query.all()


def get_due_today_tasks(user_id):
    """Return pending tasks due today."""
    today = date.today()

    return (
        Task.query
        .filter(
            Task.user_id == user_id,
            Task.status == "PENDING",
            Task.due_date == today
        )
        .order_by(Task.due_time.asc())
        .all()
    )


def get_overdue_tasks(user_id):
    """Return pending tasks whose deadline has already passed."""
    now = datetime.now()
    today = now.date()
    current_time = now.time()

    tasks = (
        Task.query
        .filter(
            Task.user_id == user_id,
            Task.status == "PENDING",
            Task.due_date <= today
        )
        .order_by(Task.due_date.asc(), Task.due_time.asc())
        .all()
    )

    overdue_tasks = []

    for task in tasks:
        if task.due_date < today:
            overdue_tasks.append(task)

        elif task.due_date == today:
            if task.due_time is None:
                overdue_tasks.append(task)
            elif task.due_time < current_time:
                overdue_tasks.append(task)

    return overdue_tasks


def is_task_overdue(task):
    """Check whether a single task is overdue."""
    if task.status != "PENDING":
        return False

    now = datetime.now()

    if task.due_date < now.date():
        return True

    if task.due_date > now.date():
        return False

    if task.due_time is None:
        return True

    return task.due_time < now.time()