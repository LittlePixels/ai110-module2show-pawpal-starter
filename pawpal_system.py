from dataclasses import dataclass, field


@dataclass
class Task:
    description: str
    time: str
    frequency: str
    completed: bool = False

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def is_due(self) -> bool:
        """Return True if the task has not yet been completed."""
        return not self.completed


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


class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize the scheduler with an owner to manage."""
        self._owner = owner

    def get_all_tasks(self) -> list:
        """Retrieve all tasks from the owner's pets."""
        return self._owner.get_all_tasks()

    def get_pending_tasks(self) -> list:
        """Return only tasks that have not yet been completed."""
        return [(pet_name, task) for pet_name, task in self.get_all_tasks() if task.is_due()]

    def prioritize_tasks(self) -> list:
        """Return pending tasks sorted by scheduled time."""
        return sorted(self.get_pending_tasks(), key=lambda entry: entry[1].time)

    def run(self):
        """Print today's schedule sorted by time to the terminal."""
        print("=" * 40)
        print("       TODAY'S SCHEDULE - PawPal+")
        print("=" * 40)
        schedule = self.prioritize_tasks()
        if not schedule:
            print("No pending tasks for today!")
        for pet_name, task in schedule:
            status = "Done" if task.completed else "Pending"
            print(f"  [{task.time}] {pet_name} - {task.description} ({task.frequency}) | {status}")
        print("=" * 40)
