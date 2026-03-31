from dataclasses import dataclass, field
from datetime import datetime, date, timedelta

# Maps frequency labels to how many days until the next occurrence
RECURRENCE_DAYS = {"Daily": 1, "Weekly": 7, "Monthly": 30}


@dataclass
class Task:
    description: str
    time: str
    frequency: str
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def is_due(self) -> bool:
        """Return True if the task is pending and due on or before today."""
        return not self.completed and self.due_date <= date.today()


@dataclass
class Pet:
    name: str
    species: str
    location: str
    type_of_food: str
    type_of_shampoo: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> list:
        """Return all tasks assigned to this pet."""
        return self.tasks

    def walk_on_leash(self):
        """Walk the pet on a leash at the assigned location."""
        pass

    def eat_food(self):
        """Feed the pet its assigned type of food."""
        pass

    def bath_in_water(self):
        """Bathe the pet using its assigned shampoo."""
        pass


@dataclass
class Owner:
    name: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Register a pet under this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list:
        """Return all tasks across every pet as (pet_name, task) tuples."""
        all_tasks = []
        for pet in self.pets:
            for task in pet.get_tasks():
                all_tasks.append((pet.name, task))
        return all_tasks

    def find_pet(self, pet_name: str):
        """Return the Pet object matching the given name, or None."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None


class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize the scheduler with an owner to manage."""
        self._owner = owner

    def get_all_tasks(self) -> list:
        """Retrieve all tasks from the owner's pets."""
        return self._owner.get_all_tasks()

    def get_pending_tasks(self) -> list:
        """Return only tasks that are pending and due today or earlier."""
        return [(pet_name, task) for pet_name, task in self.get_all_tasks() if task.is_due()]

    def filter_by_status(self, completed: bool) -> list:
        """Return tasks matching the given completion status across all pets."""
        return [(pet_name, task) for pet_name, task in self.get_all_tasks()
                if task.completed == completed]

    def filter_by_pet(self, pet_name: str) -> list:
        """Return all tasks belonging to a specific pet by name."""
        return [(p, task) for p, task in self.get_all_tasks() if p == pet_name]

    def prioritize_tasks(self) -> list:
        """Return pending tasks sorted by scheduled time."""
        return sorted(
            self.get_pending_tasks(),
            key=lambda entry: datetime.strptime(entry[1].time, "%H:%M")
        )

    def detect_conflicts(self) -> list:
        """Return warning strings for any two pending tasks scheduled at the same time."""
        warnings = []
        seen = {}  # time -> (pet_name, task)
        for pet_name, task in self.prioritize_tasks():
            if task.time in seen:
                prev_pet, prev_task = seen[task.time]
                warnings.append(
                    f"CONFLICT at {task.time}: '{prev_task.description}' ({prev_pet}) "
                    f"and '{task.description}' ({pet_name}) overlap."
                )
            else:
                seen[task.time] = (pet_name, task)
        return warnings

    def mark_task_complete(self, pet_name: str, task: Task):
        """Mark a task complete and auto-schedule the next occurrence using timedelta."""
        task.mark_complete()

        days_ahead = RECURRENCE_DAYS.get(task.frequency)
        if days_ahead:
            next_due = date.today() + timedelta(days=days_ahead)
            next_task = Task(
                description=task.description,
                time=task.time,
                frequency=task.frequency,
                due_date=next_due,
            )
            pet = self._owner.find_pet(pet_name)
            if pet:
                pet.add_task(next_task)

    def run(self):
        """Print today's schedule sorted by time to the terminal, with conflict warnings."""
        print("=" * 40)
        print("       TODAY'S SCHEDULE - PawPal+")
        print("=" * 40)
        schedule = self.prioritize_tasks()
        if not schedule:
            print("No pending tasks for today!")
        for pet_name, task in schedule:
            print(f"  [{task.time}] {pet_name} - {task.description} ({task.frequency}) | due {task.due_date}")
        conflicts = self.detect_conflicts()
        if conflicts:
            print()
            for warning in conflicts:
                print(f"  [!] {warning}")
        print("=" * 40)
