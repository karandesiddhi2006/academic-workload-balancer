
from datetime import date

from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models import Task

from app.services.deadline_service import (
    get_upcoming_tasks,
    get_due_today_tasks,
    get_overdue_tasks,
)

from app.services.workload_service import (
    calculate_daily_workload,
    get_high_workload_days,
)

from app.services.cluster_service import detect_deadline_clusters


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def home():

    # TASK STATISTICS
    pending_count = Task.query.filter_by(
        user_id=current_user.id,
        status="PENDING",
    ).count()

    completed_count = Task.query.filter_by(
        user_id=current_user.id,
        status="COMPLETED",
    ).count()

    # DEADLINE INFORMATION
    upcoming_tasks = get_upcoming_tasks(
        current_user.id,
        limit=5,
    )

    due_today_tasks = get_due_today_tasks(current_user.id)

    overdue_tasks = get_overdue_tasks(current_user.id)

    # WORKLOAD ANALYSIS
    daily_workload = calculate_daily_workload(current_user.id)

    high_workload_days = get_high_workload_days(current_user.id)

    # TODAY'S WORKLOAD
    today = date.today()

    today_workload = daily_workload.get(
        today,
        {
            "workload_points": 0,
            "task_count": 0,
            "workload_level": "LOW",
            "tasks": [],
        },
    )

    # DEADLINE CLUSTER DETECTION
    deadline_clusters = detect_deadline_clusters(current_user.id)

    # RENDER DASHBOARD
    return render_template(
        "dashboard.html",
        user=current_user,
        pending_count=pending_count,
        completed_count=completed_count,
        due_today_count=len(due_today_tasks),
        overdue_count=len(overdue_tasks),
        upcoming_tasks=upcoming_tasks,
        overdue_tasks=overdue_tasks,
        daily_workload=daily_workload,
        high_workload_days=high_workload_days,
        today_workload=today_workload,
        deadline_clusters=deadline_clusters,
    )
