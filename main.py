from datetime import date
from pawpal_system import Task, Pet, Owner

# ── Owner ────────────────────────────────────────────────────────────────────

owner = Owner("Patricia", "Khisa")

# ── Tasks ────────────────────────────────────────────────────────────────────

task1 = Task("Walking",   20, "high", "Just go on a little walk", "daily",        False)
task2 = Task("Running",   40, "low",  "A run by the beach",       "once a month", False)
task3 = Task("Bath Time", 30, "high", "Get all cleaned up",       "once a week",  False)

# ── Pets ─────────────────────────────────────────────────────────────────────

pet1 = Pet("Buddy", 2, "female", "Golden Retriever", tasks=[task1, task2])
pet2 = Pet("Loice", 9, "male",   "Bulldog",          tasks=[task3])

owner.add_pet(pet1)
owner.add_pet(pet2)

# ── Print Today's Schedule ───────────────────────────────────────────────────

W = 44
today = date.today().strftime("%B %d, %Y")

print("=" * W)
print("      PAWPAL - TODAY'S SCHEDULE")
print(f"             {today}")
print("=" * W)
print(f"  Owner: {owner.full_name()}")

for pet in owner.pets:
    sex_label = "F" if pet.sex.lower() == "female" else "M"
    print()
    print(f"  {pet.name} | {pet.breed} | Age: {pet.age} | {sex_label}")
    print("  " + "." * (W - 2))
    for task in pet.tasks:
        status = "[x]" if task.completed else "[ ]"
        print(f"  {status} {task.title:<16} {task.duration_minutes} min  "
              f"{task.priority.upper():<6}  {task.frequency}")
        print(f"      {task.description}")

all_tasks = owner.get_all_tasks()
completed_count = sum(1 for t in all_tasks if t.completed)

print()
print("=" * W)
print(f"  Tasks: {len(all_tasks)} total  |  Completed: {completed_count}")
print("=" * W)
