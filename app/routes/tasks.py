from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.models import Task, Subject


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("/")
@login_required
def list_tasks():

    tasks = (
        Task.query
        .filter_by(user_id=current_user.id)
        .order_by(Task.due_date.asc(), Task.due_time.asc())
        .all()
    )

    return render_template(
        "tasks.html",
        tasks=tasks
    )


@tasks_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_task():

    subjects = (
        Subject.query
        .filter_by(user_id=current_user.id)
        .order_by(Subject.name.asc())
        .all()
    )

    if not subjects:
        flash(
            "Please add at least one subject before creating a task.",
            "error"
        )
        return redirect(url_for("subjects.add_subject"))

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        subject_id = request.form.get("subject_id")
        task_type = request.form.get("task_type")
        priority = request.form.get("priority")
        due_date = request.form.get("due_date")
        due_time = request.form.get("due_time")
        estimated_effort = request.form.get("estimated_effort")

        if not title or not subject_id or not task_type or not priority or not due_date:
            flash(
                "Please fill in all required fields.",
                "error"
            )
            return redirect(url_for("tasks.add_task"))

        subject = Subject.query.filter_by(
            id=subject_id,
            user_id=current_user.id
        ).first()

        if not subject:
            flash("Invalid subject selected.", "error")
            return redirect(url_for("tasks.add_task"))

        task = Task(
            title=title,
            description=description if description else None,
            subject_id=subject.id,
            user_id=current_user.id,
            task_type=task_type,
            priority=priority,
            due_date=datetime.strptime(due_date, "%Y-%m-%d").date(),
            due_time=(
                datetime.strptime(due_time, "%H:%M").time()
                if due_time else None
            ),
            estimated_effort=(
                float(estimated_effort)
                if estimated_effort else None
            ),
            status="PENDING"
        )

        db.session.add(task)
        db.session.commit()

        flash("Task added successfully.", "success")

        return redirect(url_for("tasks.list_tasks"))

    return render_template(
        "add_task.html",
        subjects=subjects
    )


@tasks_bp.route("/edit/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):

    task = Task.query.filter_by(
        id=task_id,
        user_id=current_user.id
    ).first_or_404()

    subjects = (
        Subject.query
        .filter_by(user_id=current_user.id)
        .order_by(Subject.name.asc())
        .all()
    )

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        subject_id = request.form.get("subject_id")
        task_type = request.form.get("task_type")
        priority = request.form.get("priority")
        due_date = request.form.get("due_date")
        due_time = request.form.get("due_time")
        estimated_effort = request.form.get("estimated_effort")

        if not title or not subject_id or not task_type or not priority or not due_date:
            flash(
                "Please fill in all required fields.",
                "error"
            )
            return redirect(
                url_for("tasks.edit_task", task_id=task.id)
            )

        subject = Subject.query.filter_by(
            id=subject_id,
            user_id=current_user.id
        ).first()

        if not subject:
            flash("Invalid subject selected.", "error")
            return redirect(
                url_for("tasks.edit_task", task_id=task.id)
            )

        task.title = title
        task.description = description if description else None
        task.subject_id = subject.id
        task.task_type = task_type
        task.priority = priority
        task.due_date = datetime.strptime(
            due_date,
            "%Y-%m-%d"
        ).date()

        task.due_time = (
            datetime.strptime(
                due_time,
                "%H:%M"
            ).time()
            if due_time else None
        )

        task.estimated_effort = (
            float(estimated_effort)
            if estimated_effort else None
        )

        db.session.commit()

        flash("Task updated successfully.", "success")

        return redirect(url_for("tasks.list_tasks"))

    return render_template(
        "add_task.html",
        task=task,
        subjects=subjects
    )


@tasks_bp.route("/complete/<int:task_id>", methods=["POST"])
@login_required
def complete_task(task_id):

    task = Task.query.filter_by(
        id=task_id,
        user_id=current_user.id
    ).first_or_404()

    task.status = "COMPLETED"
    task.completed_at = datetime.utcnow()

    db.session.commit()

    flash("Task marked as completed.", "success")

    return redirect(url_for("tasks.list_tasks"))


@tasks_bp.route("/delete/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):

    task = Task.query.filter_by(
        id=task_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(task)
    db.session.commit()

    flash("Task deleted successfully.", "success")

    return redirect(url_for("tasks.list_tasks"))
