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

## Smarter Scheduling

The scheduler goes beyond a simple task list with four algorithmic features:

- **Time-sorted schedule** — `prioritize_tasks()` uses `datetime.strptime` with a lambda key so tasks sort correctly by `HH:MM` even when times lack a leading zero (e.g. `"9:00"` vs `"18:00"`).
- **Filtering** — `filter_by_pet(name)` and `filter_by_status(completed)` let you slice the full task list by pet or completion state without touching the underlying data.
- **Recurring tasks** — `mark_task_complete()` marks a task done and automatically creates the next occurrence using `timedelta`. A Daily task reappears tomorrow, Weekly in 7 days, Monthly in 30 days.
- **Conflict detection** — `detect_conflicts()` scans the sorted schedule for any two tasks sharing the same start time and returns plain-English warning strings — no exceptions raised, no schedule blocked.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirementse.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Testing PawPal+

### Run the test suite

```bash
python -m pytest
```

Or for verbose output showing each test name:

```bash
python -m pytest -v
```

### What the tests cover

25 automated tests across all four classes in `pawpal_system.py`:

| Area | Tests |
| --- | --- |
| **Task** | Defaults to pending, `mark_complete()`, `is_due()` before/after completion, future and past `due_date` |
| **Pet** | Starts with no tasks, `add_task()` for one and many tasks |
| **Owner** | Starts with no pets, `add_pet()`, `get_all_tasks()` across multiple pets |
| **Scheduler — sorting** | Tasks added out of order are returned chronologically; non-padded times (`"9:00"`) sort correctly |
| **Scheduler — recurrence** | Daily task creates next occurrence for tomorrow; Weekly for 7 days; unknown frequency creates no new task |
| **Scheduler — conflicts** | Same-time tasks produce a warning string; different times produce none; warnings never raise exceptions |
| **Scheduler — edge cases** | Owner with no pets, pet with no tasks, filter for a nonexistent pet name — all return empty lists without crashing |

### Confidence Level

### 4 / 5 stars

The core happy paths (sorting, filtering, recurrence, conflict detection) and the most likely edge cases (empty pets/tasks, unknown frequency, past/future due dates) are all covered and passing. One star is held back because conflict detection only checks for exact time matches — duration-based overlap detection is not yet tested, and the Streamlit UI layer (`app.py`) has no automated tests.
