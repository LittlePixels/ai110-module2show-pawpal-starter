import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


# --- Task Tests ---

def test_task_defaults_to_not_completed():
    task = Task(description="Morning Walk", time="07:00", frequency="Daily")
    assert task.completed is False

def test_task_mark_complete():
    task = Task(description="Feed Breakfast", time="08:00", frequency="Daily")
    task.mark_complete()
    assert task.completed is True

def test_task_is_due_when_not_completed():
    task = Task(description="Bath Time", time="17:00", frequency="Weekly")
    assert task.is_due() is True

def test_task_not_due_after_completion():
    task = Task(description="Bath Time", time="17:00", frequency="Weekly")
    task.mark_complete()
    assert task.is_due() is False


# --- Pet Tests ---

def test_pet_starts_with_no_tasks():
    pet = Pet(name="Buddy", species="Dog", location="Park",
              type_of_food="Kibble", type_of_shampoo="Oatmeal")
    assert pet.get_tasks() == []

def test_pet_add_task():
    pet = Pet(name="Buddy", species="Dog", location="Park",
              type_of_food="Kibble", type_of_shampoo="Oatmeal")
    task = Task(description="Morning Walk", time="07:00", frequency="Daily")
    pet.add_task(task)
    assert len(pet.get_tasks()) == 1

def test_pet_add_multiple_tasks():
    pet = Pet(name="Luna", species="Dog", location="Backyard",
              type_of_food="Wet Food", type_of_shampoo="Lavender")
    pet.add_task(Task(description="Walk",  time="07:00", frequency="Daily"))
    pet.add_task(Task(description="Feed",  time="08:00", frequency="Daily"))
    pet.add_task(Task(description="Bath",  time="17:00", frequency="Weekly"))
    assert len(pet.get_tasks()) == 3


# --- Owner Tests ---

def test_owner_starts_with_no_pets():
    owner = Owner(name="April")
    assert owner.pets == []

def test_owner_add_pet():
    owner = Owner(name="April")
    pet = Pet(name="Buddy", species="Dog", location="Park",
              type_of_food="Kibble", type_of_shampoo="Oatmeal")
    owner.add_pet(pet)
    assert len(owner.pets) == 1

def test_owner_get_all_tasks_across_pets():
    owner = Owner(name="April")

    buddy = Pet(name="Buddy", species="Dog", location="Park",
                type_of_food="Kibble", type_of_shampoo="Oatmeal")
    buddy.add_task(Task(description="Walk", time="07:00", frequency="Daily"))

    luna = Pet(name="Luna", species="Dog", location="Backyard",
               type_of_food="Wet Food", type_of_shampoo="Lavender")
    luna.add_task(Task(description="Feed", time="08:30", frequency="Daily"))
    luna.add_task(Task(description="Bath", time="17:00", frequency="Weekly"))

    owner.add_pet(buddy)
    owner.add_pet(luna)

    all_tasks = owner.get_all_tasks()
    assert len(all_tasks) == 3


# --- Scheduler Tests ---

def test_scheduler_get_all_tasks():
    owner = Owner(name="April")
    pet = Pet(name="Buddy", species="Dog", location="Park",
              type_of_food="Kibble", type_of_shampoo="Oatmeal")
    pet.add_task(Task(description="Walk", time="07:00", frequency="Daily"))
    pet.add_task(Task(description="Feed", time="08:00", frequency="Daily"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    assert len(scheduler.get_all_tasks()) == 2

def test_scheduler_pending_excludes_completed():
    owner = Owner(name="April")
    pet = Pet(name="Buddy", species="Dog", location="Park",
              type_of_food="Kibble", type_of_shampoo="Oatmeal")
    walk = Task(description="Walk", time="07:00", frequency="Daily")
    feed = Task(description="Feed", time="08:00", frequency="Daily")
    walk.mark_complete()
    pet.add_task(walk)
    pet.add_task(feed)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    pending = scheduler.get_pending_tasks()
    assert len(pending) == 1
    assert pending[0][1].description == "Feed"

def test_scheduler_prioritize_tasks_sorted_by_time():
    owner = Owner(name="April")
    pet = Pet(name="Buddy", species="Dog", location="Park",
              type_of_food="Kibble", type_of_shampoo="Oatmeal")
    pet.add_task(Task(description="Bath", time="17:00", frequency="Weekly"))
    pet.add_task(Task(description="Walk", time="07:00", frequency="Daily"))
    pet.add_task(Task(description="Feed", time="08:00", frequency="Daily"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    ordered = scheduler.prioritize_tasks()
    times = [task.time for _, task in ordered]
    assert times == sorted(times)


# --- Sorting Correctness ---

def test_sorting_with_non_padded_times():
    # "9:00" and "18:00" would sort wrong as plain strings ("18:00" < "9:00")
    # datetime.strptime ensures numeric ordering
    owner = Owner(name="April")
    pet = Pet(name="Buddy", species="Dog", location="Park",
              type_of_food="Kibble", type_of_shampoo="Oatmeal")
    pet.add_task(Task(description="Evening Walk", time="18:00", frequency="Daily"))
    pet.add_task(Task(description="Feed",         time="9:00",  frequency="Daily"))
    pet.add_task(Task(description="Morning Walk", time="7:00",  frequency="Daily"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    ordered = [task.description for _, task in scheduler.prioritize_tasks()]
    assert ordered == ["Morning Walk", "Feed", "Evening Walk"]


# --- Recurrence Logic ---

def test_daily_recurrence_creates_task_for_tomorrow():
    # Completing a Daily task should auto-add a new Task with due_date = today + 1
    owner = Owner(name="April")
    pet = Pet(name="Buddy", species="Dog", location="Park",
              type_of_food="Kibble", type_of_shampoo="Oatmeal")
    walk = Task(description="Morning Walk", time="7:00", frequency="Daily")
    pet.add_task(walk)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete("Buddy", walk)

    all_tasks = pet.get_tasks()
    # Original task is now done; a new one was appended
    assert len(all_tasks) == 2
    new_task = all_tasks[1]
    assert new_task.completed is False
    assert new_task.due_date == date.today() + timedelta(days=1)

def test_weekly_recurrence_creates_task_in_seven_days():
    owner = Owner(name="April")
    pet = Pet(name="Buddy", species="Dog", location="Park",
              type_of_food="Kibble", type_of_shampoo="Oatmeal")
    bath = Task(description="Bath Time", time="17:00", frequency="Weekly")
    pet.add_task(bath)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete("Buddy", bath)

    new_task = pet.get_tasks()[1]
    assert new_task.due_date == date.today() + timedelta(days=7)

def test_unknown_frequency_does_not_create_new_task():
    # If frequency is not in RECURRENCE_DAYS, no new task should be added
    owner = Owner(name="April")
    pet = Pet(name="Buddy", species="Dog", location="Park",
              type_of_food="Kibble", type_of_shampoo="Oatmeal")
    task = Task(description="Custom Task", time="10:00", frequency="Hourly")
    pet.add_task(task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete("Buddy", task)

    # Only the original completed task — no new one added
    assert len(pet.get_tasks()) == 1


# --- Conflict Detection ---

def test_no_conflicts_when_times_differ():
    owner = Owner(name="April")
    pet = Pet(name="Buddy", species="Dog", location="Park",
              type_of_food="Kibble", type_of_shampoo="Oatmeal")
    pet.add_task(Task(description="Walk", time="7:00",  frequency="Daily"))
    pet.add_task(Task(description="Feed", time="8:00",  frequency="Daily"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    assert scheduler.detect_conflicts() == []

def test_conflict_detected_for_same_time_different_pets():
    # Both pets have a task at 8:00 — should produce one conflict warning
    owner = Owner(name="April")
    buddy = Pet(name="Buddy", species="Dog", location="Park",
                type_of_food="Kibble", type_of_shampoo="Oatmeal")
    luna = Pet(name="Luna", species="Dog", location="Backyard",
               type_of_food="Wet Food", type_of_shampoo="Lavender")
    buddy.add_task(Task(description="Feed Breakfast", time="8:00", frequency="Daily"))
    luna.add_task(Task(description="Feed Breakfast",  time="8:00", frequency="Daily"))
    owner.add_pet(buddy)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert "8:00" in conflicts[0]

def test_conflict_warning_is_string_not_exception():
    # detect_conflicts() must return a list of strings — never raise
    owner = Owner(name="April")
    pet = Pet(name="Buddy", species="Dog", location="Park",
              type_of_food="Kibble", type_of_shampoo="Oatmeal")
    pet.add_task(Task(description="Task A", time="9:00", frequency="Daily"))
    pet.add_task(Task(description="Task B", time="9:00", frequency="Daily"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert isinstance(conflicts, list)
    assert all(isinstance(w, str) for w in conflicts)


# --- Edge Cases ---

def test_scheduler_with_no_pets_does_not_crash():
    owner = Owner(name="April")
    scheduler = Scheduler(owner)
    assert scheduler.get_pending_tasks() == []
    assert scheduler.detect_conflicts() == []

def test_pet_with_no_tasks_returns_empty_filter():
    owner = Owner(name="April")
    pet = Pet(name="Buddy", species="Dog", location="Park",
              type_of_food="Kibble", type_of_shampoo="Oatmeal")
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    assert scheduler.filter_by_pet("Buddy") == []

def test_filter_by_nonexistent_pet_returns_empty():
    owner = Owner(name="April")
    scheduler = Scheduler(owner)
    assert scheduler.filter_by_pet("Ghost") == []

def test_task_with_future_due_date_is_not_due():
    future = date.today() + timedelta(days=5)
    task = Task(description="Future Task", time="9:00", frequency="Weekly",
                due_date=future)
    assert task.is_due() is False

def test_task_with_past_due_date_is_due():
    past = date.today() - timedelta(days=3)
    task = Task(description="Overdue Task", time="9:00", frequency="Daily",
                due_date=past)
    assert task.is_due() is True
