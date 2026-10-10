from types import SimpleNamespace

from app.services.workload_service import (
    calculate_task_workload,
    get_workload_level
)


def create_task(task_type, priority):
    return SimpleNamespace(
        task_type=task_type,
        priority=priority
    )


def test_assignment_low_workload():
    task = create_task("Assignment", "LOW")

    assert calculate_task_workload(task) == 2


def test_practical_high_workload():
    task = create_task("Practical", "HIGH")

    assert calculate_task_workload(task) == 6


def test_test_medium_workload():
    task = create_task("Test", "MEDIUM")

    assert calculate_task_workload(task) == 4.5


def test_project_high_workload():
    task = create_task("Project", "HIGH")

    assert calculate_task_workload(task) == 8


def test_low_workload_level():
    assert get_workload_level(3) == "LOW"


def test_medium_workload_level():
    assert get_workload_level(5) == "MEDIUM"


def test_high_workload_level():
    assert get_workload_level(8) == "HIGH"