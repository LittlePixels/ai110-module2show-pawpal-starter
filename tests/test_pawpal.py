import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
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
