from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler

# ── Owner ────────────────────────────────────────────────────────────────────

owner = Owner("Patricia", "Khisa")

# ── Tasks (added out of order intentionally) ─────────────────────────────────

task1 = Task("Bath Time",     30, "high",   "Get all cleaned up",       "daily",        False)
task2 = Task("Evening Walk",  25, "low",    "Calm walk before bed",     "daily",        False)
task3 = Task("Feeding",       10, "high",   "Morning meal",             "daily",        False)
task4 = Task("Grooming",      20, "medium", "Brush coat thoroughly",    "daily",        False)
task5 = Task("Running",       40, "low",    "A run by the beach",       "once a month", False)
task6 = Task("Vet Checkup",   60, "medium", "Annual checkup",           "weekly",       False)

# ── Pets ─────────────────────────────────────────────────────────────────────

# Buddy gets tasks added out of order (low before high)
pet1 = Pet("Buddy", 2, "female", "Golden Retriever")
pet1.add_task(task2)   # low  — added first
pet1.add_task(task5)   # low  — monthly, should be filtered out
pet1.add_task(task3)   # high — added third
pet1.add_task(task4)   # medium

# Loice gets different tasks
pet2 = Pet("Loice", 9, "male", "Bulldog")
pet2.add_task(task1)   # high
pet2.add_task(task6)   # medium — weekly, should be filtered out

owner.add_pet(pet1)
owner.add_pet(pet2)

# ── Scheduler ────────────────────────────────────────────────────────────────

scheduler = Scheduler()

W = 44
today = date.today().strftime("%B %d, %Y")

print("=" * W)
print("      PAWPAL - SORT & FILTER TEST")
print(f"             {today}")
print("=" * W)
print(f"  Owner: {owner.full_name()}")

# ── Test filter_tasks_by_pet ─────────────────────────────────────────────────

for pet_name in ["Buddy", "Loice"]:
    filtered = scheduler.filter_tasks_by_pet(owner.pets, pet_name)
    print()
    print(f"  filter_tasks_by_pet -> '{pet_name}' ({len(filtered)} task(s)):")
    for t in filtered:
        print(f"    - {t.title:<16} | {t.priority:<6} | {t.frequency}")

# ── Test generate_schedule (applies daily filter + priority sort + time sort) ─

print()
print("=" * W)
print("  GENERATED SCHEDULES (daily tasks only, priority-sorted)")
print("=" * W)

for pet in owner.pets:
    schedule = scheduler.generate_schedule(
        owner,
        pet,
        pet.tasks,
        available_minutes=60,
        start_time="08:00 AM",
    )
    print()
    print(schedule.display())

# ── Test detect_conflicts ────────────────────────────────────────────────────

print()
print("=" * W)
print("  CONFLICT DETECTION TEST")
print("=" * W)

from pawpal_system import ScheduledTask

# Two tasks that overlap: 08:00-08:30 and 08:15-08:45
conflict_a = ScheduledTask(task=task1, start_time="08:00 AM", end_time="08:30 AM", reason="test")
conflict_b = ScheduledTask(task=task4, start_time="08:15 AM", end_time="08:45 AM", reason="test")
# One task that does not overlap: 08:45-09:00
no_conflict = ScheduledTask(task=task3, start_time="08:45 AM", end_time="09:00 AM", reason="test")

conflicts = scheduler.detect_conflicts([conflict_a, conflict_b, no_conflict])

print()
if conflicts:
    for warning in conflicts:
        print(f"  WARNING: {warning}")
else:
    print("  No conflicts detected.")

# ── Test reschedule_completed_tasks ─────────────────────────────────────────

print()
print("=" * W)
print("  RESCHEDULE TEST")
print("=" * W)

# Mark Buddy's daily tasks as complete
task3.mark_complete()  # Feeding (daily)
task4.mark_complete()  # Grooming (daily)
task5.mark_complete()  # Running (once a month — should NOT be rescheduled)

print()
print("  Marking Feeding, Grooming, Running as complete for Buddy...")
new_tasks = scheduler.reschedule_completed_tasks(pet1)

print(f"  New tasks created: {len(new_tasks)}")
for t in new_tasks:
    print(f"    - {t.title:<16} | completed={t.completed} | frequency={t.frequency}")

# ── Summary ──────────────────────────────────────────────────────────────────

all_tasks = owner.get_all_tasks()
completed_count = sum(1 for t in all_tasks if t.completed)

print()
print("=" * W)
print(f"  Total tasks across all pets : {len(all_tasks)}")
print(f"  Completed                   : {completed_count}")
print("=" * W)
