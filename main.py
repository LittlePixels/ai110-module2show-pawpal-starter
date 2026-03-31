from pawpal_system import Task, Pet, Owner, Scheduler

owner = Owner(name="April")

buddy = Pet(name="Buddy", species="Dog", location="Riverside Park",
            type_of_food="Dry Kibble", type_of_shampoo="Oatmeal Shampoo")

luna = Pet(name="Luna", species="Dog", location="Backyard",
           type_of_food="Wet Food", type_of_shampoo="Lavender Shampoo")

buddy.add_task(Task(description="Morning Walk",   time="7:00",  frequency="Daily"))
buddy.add_task(Task(description="Feed Breakfast", time="8:00",  frequency="Daily"))
buddy.add_task(Task(description="Bath Time",      time="17:00", frequency="Weekly"))

luna.add_task(Task(description="Feed Breakfast",  time="8:00",  frequency="Daily"))  # conflicts with Buddy at 8:00
luna.add_task(Task(description="Evening Walk",    time="18:00", frequency="Daily"))
luna.add_task(Task(description="Vet Checkup",     time="17:00", frequency="Monthly"))  # conflicts with Buddy at 17:00

owner.add_pet(buddy)
owner.add_pet(luna)

scheduler = Scheduler(owner)
scheduler.run()
