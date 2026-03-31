from pawpal_system import Task, Pet, Owner, Scheduler

# --- Create Owner ---
owner = Owner(name="April")

# --- Create Pets ---
buddy = Pet(
    name="Buddy",
    species="Dog",
    location="Riverside Park",
    type_of_food="Dry Kibble",
    type_of_shampoo="Oatmeal Shampoo",
)

luna = Pet(
    name="Luna",
    species="Dog",
    location="Backyard",
    type_of_food="Wet Food",
    type_of_shampoo="Lavender Shampoo",
)

# --- Create Tasks ---
buddy.add_task(Task(description="Morning Walk",  time="07:00", frequency="Daily"))
buddy.add_task(Task(description="Feed Breakfast", time="08:00", frequency="Daily"))
buddy.add_task(Task(description="Bath Time",      time="17:00", frequency="Weekly"))

luna.add_task(Task(description="Feed Breakfast",  time="08:30", frequency="Daily"))
luna.add_task(Task(description="Evening Walk",    time="18:00", frequency="Daily"))

# --- Register Pets with Owner ---
owner.add_pet(buddy)
owner.add_pet(luna)

# --- Run Scheduler ---
scheduler = Scheduler(owner)
scheduler.run()
