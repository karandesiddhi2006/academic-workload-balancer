from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.models import Subject

subjects_bp = Blueprint("subjects", __name__, url_prefix="/subjects")


@subjects_bp.route("/")
@login_required
def list_subjects():
    subjects = (
        Subject.query
        .filter_by(user_id=current_user.id)
        .order_by(Subject.name.asc())
        .all()
    )

    return render_template(
        "subjects.html",
        subjects=subjects
    )


@subjects_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_subject():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        code = request.form.get("code", "").strip()

        if not name:
            flash("Subject name is required.", "error")
            return redirect(url_for("subjects.add_subject"))

        subject = Subject(
            name=name,
            code=code if code else None,
            user_id=current_user.id
        )

        db.session.add(subject)
        db.session.commit()

        flash("Subject added successfully.", "success")

        return redirect(url_for("subjects.list_subjects"))

    return render_template("add_subject.html")


@subjects_bp.route("/edit/<int:subject_id>", methods=["GET", "POST"])
@login_required
def edit_subject(subject_id):

    subject = Subject.query.filter_by(
        id=subject_id,
        user_id=current_user.id
    ).first_or_404()

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        code = request.form.get("code", "").strip()

        if not name:
            flash("Subject name is required.", "error")
            return redirect(
                url_for("subjects.edit_subject", subject_id=subject.id)
            )

        subject.name = name
        subject.code = code if code else None

        db.session.commit()

        flash("Subject updated successfully.", "success")

        return redirect(url_for("subjects.list_subjects"))

    return render_template(
        "add_subject.html",
        subject=subject
    )


@subjects_bp.route("/delete/<int:subject_id>", methods=["POST"])
@login_required
def delete_subject(subject_id):

    subject = Subject.query.filter_by(
        id=subject_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(subject)
    db.session.commit()

    flash("Subject deleted successfully.", "success")

    return redirect(url_for("subjects.list_subjects"))