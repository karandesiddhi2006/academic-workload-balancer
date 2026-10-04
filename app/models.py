from datetime import datetime

from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subjects = db.relationship(
        "Subject",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    tasks = db.relationship(
        "Task",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    workload_analyses = db.relationship(
        "WorkloadAnalysis",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    deadline_clusters = db.relationship(
        "DeadlineCluster",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )


class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), nullable=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tasks = db.relationship(
        "Task",
        backref="subject",
        lazy=True,
        cascade="all, delete-orphan"
    )


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    task_type = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(20), nullable=False)

    due_date = db.Column(db.Date, nullable=False)
    due_time = db.Column(db.Time, nullable=True)

    estimated_effort = db.Column(db.Float, nullable=True)

    status = db.Column(
        db.String(20),
        nullable=False,
        default="PENDING"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    completed_at = db.Column(db.DateTime, nullable=True)


class WorkloadAnalysis(db.Model):
    __tablename__ = "workload_analyses"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    analysis_date = db.Column(db.Date, nullable=False)

    workload_points = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    workload_level = db.Column(
        db.String(20),
        nullable=False
    )

    task_count = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class DeadlineCluster(db.Model):
    __tablename__ = "deadline_clusters"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    task_count = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    total_workload = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )