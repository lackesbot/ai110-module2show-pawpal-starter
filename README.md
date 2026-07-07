# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## ✨ Features

- **Priority-based sorting** — `Scheduler.generate_schedule()` orders pending tasks high → medium → low, so the most important care tasks always get placed first when time is tight.
- **Time-budget fitting** — Tasks are greedily added to the schedule until the owner's available minutes run out; anything that doesn't fit (starting with the lowest priority) is left off rather than crammed in.
- **Chronological sorting** — `Scheduler.sort_by_time()` re-orders any list of scheduled tasks by `start_time`, guaranteeing the final plan always reads top-to-bottom in time order regardless of how it was built.
- **Conflict warnings** — `Scheduler.detect_conflicts()` checks every pair of scheduled tasks for overlapping time windows (`a_start < b_end and b_start < a_end`) and returns a human-readable warning for each overlap found.
- **Daily recurrence** — `Task.next_occurrence()` + `Scheduler.reschedule_completed_tasks()` automatically generate a fresh, incomplete copy of any `"daily"` or `"weekly"` task once it's marked done, so recurring care never has to be re-entered by hand.
- **Per-pet task filtering** — `Scheduler.filter_tasks_by_pet()` isolates one pet's tasks from the owner's full list by name, so multi-pet households get a separate schedule per animal.
- **Frequency-aware scheduling** — only `"daily"` tasks are pulled into a given schedule run; `"weekly"` and `"as needed"` tasks are excluded so one-off or infrequent items don't crowd out the daily routine.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.


## Sample Output
A run by the beach

  Loice | Bulldog | Age: 9 | M
  ..........................................
  [ ] Bath Time        30 min  HIGH    once a week
      Get all cleaned up



## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

**Core behavior**
- `mark_complete()` flips a task's status from incomplete to done
- `add_task()` correctly increases a pet's task count

**Sorting correctness**
- `generate_schedule()` always places high-priority tasks before medium and low
- `sort_by_time()` orders a list of scheduled tasks chronologically regardless of input order
- Empty input to `sort_by_time()` returns an empty list without errors

**Recurrence logic**
- `next_occurrence()` produces a fresh task with `completed=False` and all original fields preserved
- Completing a `"daily"` task triggers a new instance to be added to the pet's task list
- Completing an `"as needed"` task does not trigger rescheduling
- Incomplete tasks are never rescheduled

**Conflict detection**
- Overlapping time windows are caught and a descriptive warning string is returned
- Tasks that share only a boundary (one ends exactly when the next starts) are not flagged
- Empty and single-task inputs return no warnings



```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

============================================================================================================ 13 passed in 0.09s =======================================================================================================
```
# Paste your pytest output here
```
tests\test_pawpal.py .............                                                                                                                                                                                 ======================================= 13 passed in 0.11s =======================================

Confidence level: 4 starrs 



## 📐 Smarter Scheduling

| Feature | Method | Description |
|---------|--------|-------------|
| Priority sorting | `Scheduler.generate_schedule()` | Tasks are sorted high → medium → low before scheduling so the most important tasks are always placed first |
| Time budget fitting | `Scheduler.generate_schedule()` | Tasks that would exceed the owner's available minutes are dropped, starting from the lowest priority |
| Recurring task filter | `Scheduler.generate_schedule()` | Only `"daily"` frequency tasks are included in each schedule run; weekly and one-off tasks are excluded |
| Chronological sorting | `Scheduler.sort_by_time()` | Returns a scheduled task list sorted by `start_time` so the final schedule always reads in time order |
| Filter tasks by pet | `Scheduler.filter_tasks_by_pet()` | Looks up a pet by name from the owner's pet list and returns only that pet's tasks, isolating work per animal |
| Conflict detection | `Scheduler.detect_conflicts()` | Compares every pair of scheduled tasks for overlapping time windows using the formula `a_start < b_end and b_start < a_end`, returning a warning string per conflict |
| Auto-reschedule recurring tasks | `Scheduler.reschedule_completed_tasks()` | When a `"daily"` or `"weekly"` task is marked complete, a fresh copy is automatically appended to the pet's task list via `Task.next_occurrence()` |
| Next occurrence factory | `Task.next_occurrence()` | Creates an identical Task with `completed=False`, used by `reschedule_completed_tasks()` to produce the next instance of a recurring task |



## 📸 Demo Walkthrough

### UI features

- **Owner** — a form to enter first/last name and save the current owner.
- **Add a Pet** — a form to enter a pet's name, age, breed, sex, and species; saved pets are attached to the current owner.
- **Schedule a Task** — a form to add a task with a title, duration, priority (low/medium/high), optional description, and frequency (daily/weekly/as needed). Added tasks are listed in a table, with a button to clear them all.
- **Build Schedule** — pick a pet (when the owner has more than one), set the available minutes and a start time, then click **Generate schedule** to produce a plan. Results are shown as success/warning banners plus a table of the final schedule.

### Example workflow

1. Save an owner (e.g., "Patricia Khisa").
2. Add a pet (e.g., "Buddy", a Golden Retriever) — the pet is attached to the owner.
3. Add a few tasks for Buddy: "Feeding" (10 min, high, daily), "Grooming" (20 min, medium, daily), "Evening Walk" (25 min, low, daily).
4. Select "Buddy", set available time to 60 minutes and a start time of 08:00 AM.
5. Click Generate schedule to view today's schedule — the tasks appear sorted by priority and time, with any conflicts or dropped tasks called out above the table.

### Key Scheduler behaviors shown

- **Priority sorting** — high-priority tasks (e.g., Feeding) are placed before medium and low priority tasks, regardless of the order they were added.
- **Time-budget fitting** — if the pet's tasks add up to more minutes than the owner has available, the lowest-priority tasks are dropped and called out in a warning.
- **Daily-only filtering** — only `"daily"` tasks are included in a generated schedule; `"weekly"` and `"as needed"` tasks are excluded automatically.
- **Chronological sorting** — `Scheduler.sort_by_time()` guarantees the displayed schedule always reads in time order.
- **Conflict warnings** — `Scheduler.detect_conflicts()` flags any two scheduled tasks with overlapping time windows.
- **Recurrence** — marking a `"daily"` or `"weekly"` task complete and calling `Scheduler.reschedule_completed_tasks()` automatically queues up its next occurrence.

### Sample CLI output (`python main.py`)

`main.py` exercises the same `Scheduler` logic outside the UI — adding pets/tasks out of order, then running the filter, sort, conflict-detection, and recurrence behaviors:

```
============================================
      PAWPAL - SORT & FILTER TEST
             July 07, 2026
============================================
  Owner: Patricia Khisa

  filter_tasks_by_pet -> 'Buddy' (4 task(s)):
    - Evening Walk     | low    | daily
    - Running          | low    | once a month
    - Feeding          | high   | daily
    - Grooming         | medium | daily

  filter_tasks_by_pet -> 'Loice' (2 task(s)):
    - Bath Time        | high   | daily
    - Vet Checkup      | medium | weekly

============================================
  GENERATED SCHEDULES (daily tasks only, priority-sorted)
============================================

Schedule for Buddy (owner: Patricia Khisa)
Available: 60 min | Scheduled: 55 min
--------------------------------------------------
[ ] 08:00 AM - 08:10 AM | Feeding (10 min, priority: high)
     Reason: High priority — fits within available time
[ ] 08:10 AM - 08:30 AM | Grooming (20 min, priority: medium)
     Reason: Medium priority — fits within available time
[ ] 08:30 AM - 08:55 AM | Evening Walk (25 min, priority: low)
     Reason: Low priority — fits within available time

Schedule for Loice (owner: Patricia Khisa)
Available: 60 min | Scheduled: 30 min
--------------------------------------------------
[ ] 08:00 AM - 08:30 AM | Bath Time (30 min, priority: high)
     Reason: High priority — fits within available time

============================================
  CONFLICT DETECTION TEST
============================================

  WARNING: CONFLICT: 'Bath Time' (08:00 AM-08:30 AM) overlaps with 'Grooming' (08:15 AM-08:45 AM)

============================================
  RESCHEDULE TEST
============================================

  Marking Feeding, Grooming, Running as complete for Buddy...
  New tasks created: 2
    - Feeding          | completed=False | frequency=daily
    - Grooming         | completed=False | frequency=daily

============================================
  Total tasks across all pets : 8
  Completed                   : 3
============================================
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
