from dataclasses import dataclass, field


@dataclass
class Owner:
    first_name: str
    last_name: str

    def full_name(self) -> str:
        pass


@dataclass
class Pet:
    name: str
    age: int
    sex: str
    species: str
    breed: str
    allergies: list[str] = field(default_factory=list)

    def summary(self) -> str:
        pass


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"


@dataclass
class ScheduledTask:
    task: Task
    start_time: str  # e.g. "08:00 AM"
    reason: str

    def display(self) -> str:
        pass


@dataclass
class Schedule:
    owner: Owner
    pet: Pet
    scheduled_tasks: list[ScheduledTask] = field(default_factory=list)
    summary: str = ""

    def total_duration(self) -> int:
        pass

    def display(self) -> str:
        pass


class Scheduler:
    def generate_schedule(
        self,
        owner: Owner,
        pet: Pet,
        tasks: list[Task],
        available_minutes: int,
        start_time: str,
    ) -> Schedule:
        pass

    def _build_prompt(self, owner: Owner, pet: Pet, tasks: list[Task]) -> str:
        pass

    def _parse_response(self, response: str) -> list[ScheduledTask]:
        pass
