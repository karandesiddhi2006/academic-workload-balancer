
from datetime import date, timedelta
from types import SimpleNamespace

from app.services.cluster_service import (
    build_cluster,
    detect_deadline_clusters,
)


def create_task(task_id, due_date, task_type="Assignment", priority="MEDIUM"):
    return SimpleNamespace(
        id=task_id,
        due_date=due_date,
        due_time=None,
        task_type=task_type,
        priority=priority,
    )


def test_build_cluster_calculates_workload():
    tasks = [
        create_task(1, date(2026, 10, 12), "Assignment", "LOW"),
        create_task(2, date(2026, 10, 13), "Practical", "HIGH"),
    ]

    cluster = build_cluster(tasks)

    assert cluster["task_count"] == 2
    assert cluster["start_date"] == date(2026, 10, 12)
    assert cluster["end_date"] == date(2026, 10, 13)
    assert cluster["total_workload"] == 8


def test_detect_clusters_with_no_tasks(app, db):
    with app.app_context():
        clusters = detect_deadline_clusters(9999)
        assert clusters == []

def test_detects_tasks_within_two_days(app, db):
    from datetime import date
    from types import SimpleNamespace
    from app.services.cluster_service import detect_deadline_clusters

    with app.app_context():
        from app.models import User, Subject, Task
        from werkzeug.security import generate_password_hash

        user = User(
            name="Test Student",
            email="cluster-test@example.com",
            password_hash=generate_password_hash("test-password"),
        )
        db.session.add(user)
        db.session.flush()

        subject = Subject(name="AI", user_id=user.id)
        db.session.add(subject)
        db.session.flush()

        db.session.add_all([
            Task(
                title="Assignment",
                subject_id=subject.id,
                user_id=user.id,
                task_type="Assignment",
                priority="LOW",
                due_date=date(2026, 10, 12),
                status="PENDING",
            ),
            Task(
                title="Practical",
                subject_id=subject.id,
                user_id=user.id,
                task_type="Practical",
                priority="HIGH",
                due_date=date(2026, 10, 14),
                status="PENDING",
            ),
        ])
        db.session.commit()

        clusters = detect_deadline_clusters(user.id)

        assert len(clusters) == 1
        assert clusters[0]["task_count"] == 2
        assert clusters[0]["total_workload"] == 8


def test_does_not_cluster_tasks_more_than_two_days_apart(app, db):
    from datetime import date
    from app.services.cluster_service import detect_deadline_clusters

    with app.app_context():
        from app.models import User, Subject, Task
        from werkzeug.security import generate_password_hash

        user = User(
            name="Test Student",
            email="separate-test@example.com",
            password_hash=generate_password_hash("test-password"),
        )
        db.session.add(user)
        db.session.flush()

        subject = Subject(name="AI", user_id=user.id)
        db.session.add(subject)
        db.session.flush()

        db.session.add_all([
            Task(
                title="Assignment",
                subject_id=subject.id,
                user_id=user.id,
                task_type="Assignment",
                priority="LOW",
                due_date=date(2026, 10, 12),
                status="PENDING",
            ),
            Task(
                title="Project",
                subject_id=subject.id,
                user_id=user.id,
                task_type="Project",
                priority="HIGH",
                due_date=date(2026, 10, 15),
                status="PENDING",
            ),
        ])
        db.session.commit()

        clusters = detect_deadline_clusters(user.id)

        assert clusters == []
