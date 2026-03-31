# Copilot Instructions for PawPal+

## Data Classes
Use Python `@dataclass` decorator for all data-holding objects such as `Pet` and `Task`.

```python
from dataclasses import dataclass

@dataclass
class Pet:
    name: str
    species: str

@dataclass
class Task:
    task_type: str
    scheduled_time: str
    priority: int
```

- Import `dataclass` from the `dataclasses` module at the top of the file.
- Use type annotations for every field.
- Prefer `@dataclass` over manually writing `__init__`, `__repr__`, and `__eq__`.
- Use `field(default_factory=...)` for mutable defaults like lists or dicts.
