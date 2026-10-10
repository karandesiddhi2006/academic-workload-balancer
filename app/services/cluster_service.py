
from datetime import timedelta

from app.models import Task
from app.services.workload_service import calculate_task_workload


def detect_deadline_clusters(user_id):
    """Find groups of pending tasks with deadlines within a two-day window."""

    tasks = (
        Task.query
        .filter_by(user_id=user_id, status="PENDING")
        .order_by(Task.due_date.asc(), Task.due_time.asc())
        .all()
    )

    clusters = []
    current_cluster = []

    for task in tasks:
        if not current_cluster:
            current_cluster.append(task)
            continue

        first_date = current_cluster[0].due_date

        if (task.due_date - first_date).days <= 2:
            current_cluster.append(task)
        else:
            if len(current_cluster) >= 2:
                clusters.append(build_cluster(current_cluster))

            current_cluster = [task]

    if len(current_cluster) >= 2:
        clusters.append(build_cluster(current_cluster))

    return clusters


def build_cluster(tasks):
    """Calculate the date range and workload for a cluster."""

    task_dates = [task.due_date for task in tasks]

    total_workload = sum(
        calculate_task_workload(task) for task in tasks
    )

    return {
        "start_date": min(task_dates),
        "end_date": max(task_dates),
        "task_count": len(tasks),
        "total_workload": total_workload,
        "tasks": tasks,
    }
