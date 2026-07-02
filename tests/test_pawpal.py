import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    task = Task(title="Walk", duration_minutes=30, priority="high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", age=3, sex="male", breed="Labrador")
    task = Task(title="Feed", duration_minutes=10, priority="medium")
    assert len(pet.tasks) == 0
    pet.add_task(task)
    assert len(pet.tasks) == 1
