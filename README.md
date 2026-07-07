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

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

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

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
