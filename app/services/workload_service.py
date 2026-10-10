from collections import defaultdict

from app.models import Task

from app.utils.constants import (
    TASK_TYPE_WEIGHTS,
    PRIORITY_MULTIPLIERS,
    LOW_WORKLOAD_MAX,
    MEDIUM_WORKLOAD_MAX,
    WORKLOAD_LEVEL_LOW,
    WORKLOAD_LEVEL_MEDIUM,
    WORKLOAD_LEVEL_HIGH
)


def calculate_task_workload(task):
    """
    Calculate workload points for a single task.

    Formula:
    Task Type Weight × Priority Multiplier
    """

    task_weight = TASK_TYPE_WEIGHTS.get(
        task.task_type,
        0
    )

    priority_multiplier = PRIORITY_MULTIPLIERS.get(
        task.priority,
        1
    )

    return task_weight * priority_multiplier


def get_workload_level(workload_points):
    """
    Classify workload based on total workload points.

    0–3  = LOW
    4–7  = MEDIUM
    8+   = HIGH
    """

    if workload_points <= LOW_WORKLOAD_MAX:
        return WORKLOAD_LEVEL_LOW

    if workload_points <= MEDIUM_WORKLOAD_MAX:
        return WORKLOAD_LEVEL_MEDIUM

    return WORKLOAD_LEVEL_HIGH


def get_user_pending_tasks(user_id):
    """
    Return all pending tasks belonging to a user.
    """

    return (
        Task.query
        .filter_by(
            user_id=user_id,
            status="PENDING"
        )
        .order_by(
            Task.due_date.asc(),
            Task.due_time.asc()
        )
        .all()
    )


def calculate_daily_workload(user_id):
    """
    Calculate workload for each date based on
    pending academic tasks.
    """

    tasks = get_user_pending_tasks(user_id)

    daily_data = defaultdict(
        lambda: {
            "workload_points": 0,
            "task_count": 0,
            "tasks": []
        }
    )

    for task in tasks:

        workload = calculate_task_workload(task)

        daily_data[task.due_date]["workload_points"] += workload

        daily_data[task.due_date]["task_count"] += 1

        daily_data[task.due_date]["tasks"].append(task)

    for date, data in daily_data.items():

        data["workload_level"] = get_workload_level(
            data["workload_points"]
        )

    return dict(daily_data)


def get_high_workload_days(user_id):
    """
    Return dates where workload is classified as HIGH.
    """

    daily_workload = calculate_daily_workload(
        user_id
    )

    high_workload_days = []

    for date, data in daily_workload.items():

        if data["workload_level"] == WORKLOAD_LEVEL_HIGH:

            high_workload_days.append({
                "date": date,
                "workload_points": data["workload_points"],
                "task_count": data["task_count"],
                "workload_level": data["workload_level"],
                "tasks": data["tasks"]
            })

    high_workload_days.sort(
        key=lambda item: item["date"]
    )

    return high_workload_days


def get_weekly_workload(user_id):
    """
    Return workload analysis for the current week.

    The week starts on Monday and ends on Sunday.
    """

    from datetime import date, timedelta

    daily_workload = calculate_daily_workload(
        user_id
    )

    today = date.today()

    week_start = today - timedelta(
        days=today.weekday()
    )

    week_end = week_start + timedelta(days=6)

    weekly_data = []

    current_date = week_start

    while current_date <= week_end:

        data = daily_workload.get(
            current_date,
            {
                "workload_points": 0,
                "task_count": 0,
                "workload_level": "LOW",
                "tasks": []
            }
        )

        weekly_data.append({
            "date": current_date,
            "workload_points": data["workload_points"],
            "task_count": data["task_count"],
            "workload_level": data["workload_level"]
        })

        current_date += timedelta(days=1)

    return weekly_data