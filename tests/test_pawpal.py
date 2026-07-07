import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet, Owner, Scheduler, ScheduledTask


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


# ── Sorting Correctness ───────────────────────────────────────────────────────

def test_generate_schedule_sorts_high_priority_first():
    owner = Owner(first_name="Jordan", last_name="Smith")
    pet = Pet(name="Mochi", age=2, sex="female", breed="Shiba")
    pet.add_task(Task(title="Low task",    duration_minutes=10, priority="low",    frequency="daily"))
    pet.add_task(Task(title="High task",   duration_minutes=10, priority="high",   frequency="daily"))
    pet.add_task(Task(title="Medium task", duration_minutes=10, priority="medium", frequency="daily"))

    schedule = Scheduler().generate_schedule(owner, pet, pet.tasks, available_minutes=60, start_time="08:00 AM")
    titles = [st.task.title for st in schedule.scheduled_tasks]

    assert titles == ["High task", "Medium task", "Low task"]


def test_sort_by_time_orders_chronologically():
    task = Task(title="X", duration_minutes=10, priority="low")
    a = ScheduledTask(task=task, start_time="09:00 AM", end_time="09:10 AM", reason="")
    b = ScheduledTask(task=task, start_time="08:00 AM", end_time="08:10 AM", reason="")
    c = ScheduledTask(task=task, start_time="10:00 AM", end_time="10:10 AM", reason="")

    sorted_tasks = Scheduler().sort_by_time([a, b, c])
    start_times = [s.start_time for s in sorted_tasks]

    assert start_times == ["08:00 AM", "09:00 AM", "10:00 AM"]


def test_sort_by_time_empty_list_returns_empty():
    assert Scheduler().sort_by_time([]) == []


# ── Recurrence Logic ─────────────────────────────────────────────────────────

def test_next_occurrence_resets_completed_to_false():
    task = Task(title="Walk", duration_minutes=20, priority="high", frequency="daily")
    task.mark_complete()
    next_task = task.next_occurrence()

    assert next_task.completed is False
    assert next_task.title == task.title
    assert next_task.frequency == task.frequency


def test_reschedule_adds_new_task_for_daily():
    pet = Pet(name="Buddy", age=3, sex="male", breed="Labrador")
    task = Task(title="Feed", duration_minutes=10, priority="high", frequency="daily")
    pet.add_task(task)
    task.mark_complete()

    new_tasks = Scheduler().reschedule_completed_tasks(pet)

    assert len(new_tasks) == 1
    assert new_tasks[0].completed is False


def test_reschedule_skips_as_needed_tasks():
    pet = Pet(name="Buddy", age=3, sex="male", breed="Labrador")
    task = Task(title="Vet", duration_minutes=60, priority="high", frequency="as needed")
    pet.add_task(task)
    task.mark_complete()

    new_tasks = Scheduler().reschedule_completed_tasks(pet)

    assert len(new_tasks) == 0


def test_reschedule_does_not_affect_incomplete_tasks():
    pet = Pet(name="Buddy", age=3, sex="male", breed="Labrador")
    task = Task(title="Walk", duration_minutes=20, priority="medium", frequency="daily")
    pet.add_task(task)

    new_tasks = Scheduler().reschedule_completed_tasks(pet)

    assert len(new_tasks) == 0
    assert len(pet.tasks) == 1


# ── Conflict Detection ────────────────────────────────────────────────────────

def test_detect_conflicts_finds_overlapping_tasks():
    task = Task(title="X", duration_minutes=30, priority="high")
    a = ScheduledTask(task=task, start_time="08:00 AM", end_time="08:30 AM", reason="")
    b = ScheduledTask(task=task, start_time="08:15 AM", end_time="08:45 AM", reason="")

    conflicts = Scheduler().detect_conflicts([a, b])

    assert len(conflicts) == 1
    assert "08:00 AM" in conflicts[0]


def test_detect_conflicts_no_conflict_when_tasks_touch_boundary():
    task = Task(title="X", duration_minutes=30, priority="high")
    a = ScheduledTask(task=task, start_time="08:00 AM", end_time="08:30 AM", reason="")
    b = ScheduledTask(task=task, start_time="08:30 AM", end_time="09:00 AM", reason="")

    conflicts = Scheduler().detect_conflicts([a, b])

    assert len(conflicts) == 0


def test_detect_conflicts_empty_list_returns_no_warnings():
    assert Scheduler().detect_conflicts([]) == []


def test_detect_conflicts_single_task_returns_no_warnings():
    task = Task(title="X", duration_minutes=10, priority="low")
    a = ScheduledTask(task=task, start_time="08:00 AM", end_time="08:10 AM", reason="")

    assert Scheduler().detect_conflicts([a]) == []
