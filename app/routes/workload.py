
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.services.workload_service import (
    calculate_daily_workload,
    get_high_workload_days,
    get_weekly_workload,
)
from app.services.cluster_service import detect_deadline_clusters

workload_bp = Blueprint("workload", __name__, url_prefix="/workload")


@workload_bp.route("/")
@login_required
def workload_dashboard():
    daily_workload = calculate_daily_workload(current_user.id)
    high_workload_days = get_high_workload_days(current_user.id)
    weekly_workload = get_weekly_workload(current_user.id)
    deadline_clusters = detect_deadline_clusters(current_user.id)

    return render_template(
        "workload.html",
        daily_workload=daily_workload,
        high_workload_days=high_workload_days,
        weekly_workload=weekly_workload,
        deadline_clusters=deadline_clusters,
    )
