from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.services.deadline_service import (
    get_upcoming_tasks,
    get_due_today_tasks,
    get_overdue_tasks
)

deadlines_bp = Blueprint(
    "deadlines",
    __name__,
    url_prefix="/deadlines"
)


@deadlines_bp.route("/")
@login_required
def deadline_dashboard():
    upcoming_tasks = get_upcoming_tasks(current_user.id)
    due_today_tasks = get_due_today_tasks(current_user.id)
    overdue_tasks = get_overdue_tasks(current_user.id)

    return render_template(
        "deadlines.html",
        upcoming_tasks=upcoming_tasks,
        due_today_tasks=due_today_tasks,
        overdue_tasks=overdue_tasks
    )