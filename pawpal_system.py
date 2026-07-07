from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str           # "low", "medium", "high"
    description: str = ""
    frequency: str = "daily"  # e.g. "daily", "weekly", "as needed"
    completed: bool = False

    def mark_complete(self) -> None:
        """Sets the task's completed flag to True, permanently marking it as done regardless of prior state."""
        self.completed = True

    def next_occurrence(self) -> "Task":
        """Returns a new identical Task with completed reset to False, for rescheduling daily or weekly tasks."""
        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            description=self.description,
            frequency=self.frequency,
            completed=False,
        )


@dataclass
class Pet:
    name: str
    age: int
    sex: str
    breed: str
    tasks: list[Task] = field(default_factory=list)

    def summary(self) -> str:
        """Returns a human-readable sentence describing the pet's name, age, sex, breed, species, and known allergies."""
        allergy_info = ", ".join(self.allergies) if self.allergies else "none"
        return (
            f"{self.name} is a {self.age}-year-old {self.sex} {self.breed} "
            f"({self.species}). Known allergies: {allergy_info}."
        )

    def add_task(self, task: Task) -> None:
        """Appends the given Task to this pet's task list, making it available for scheduling."""
        self.tasks.append(task)


@dataclass
class Owner:
    first_name: str
    last_name: str
    pets: list[Pet] = field(default_factory=list)

    def full_name(self) -> str:
        """Combines the owner's first and last name into a single space-separated full name string."""
        return f"{self.first_name} {self.last_name}"

    def add_pet(self, pet: Pet) -> None:
        """Adds the given Pet to this owner's pet list, registering it for task and schedule management."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Flattens and returns every Task from every pet the owner has, in pet-registration order."""
        return [task for pet in self.pets for task in pet.tasks]


@dataclass
class ScheduledTask:
    task: Task
    start_time: str  # e.g. "08:00 AM"
    end_time: str    # e.g. "08:30 AM"
    reason: str

    def display(self) -> str:
        """Formats the scheduled task as a two-line string showing completion status, time window, title, duration, priority, and scheduling reason."""
        status = "[x]" if self.task.completed else "[ ]"
        return (
            f"[{status}] {self.start_time} - {self.end_time} | "
            f"{self.task.title} ({self.task.duration_minutes} min, "
            f"priority: {self.task.priority})\n"
            f"     Reason: {self.reason}"
        )


@dataclass
class Schedule:
    owner: Owner
    pet: Pet
    available_minutes: int
    reason: str = ""
    scheduled_tasks: list[ScheduledTask] = field(default_factory=list)
    summary: str = ""

    def total_duration(self) -> int:
        """Sums the duration_minutes of every scheduled task and returns the total minutes committed in this schedule."""
        return sum(item.task.duration_minutes for item in self.scheduled_tasks)

    def display(self) -> str:
        """Renders the full schedule as a formatted multi-line string with a header, per-task lines, and an optional AI-generated summary."""
        header = (
            f"Schedule for {self.pet.name} "
            f"(owner: {self.owner.full_name()})\n"
            f"Available: {self.available_minutes} min | "
            f"Scheduled: {self.total_duration()} min\n"
            + "-" * 50
        )
        task_lines = "\n".join(item.display() for item in self.scheduled_tasks)
        footer = f"\nSummary: {self.summary}" if self.summary else ""
        return f"{header}\n{task_lines}{footer}"


class Scheduler:
    PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

    def generate_schedule(
        self,
        owner: Owner,
        pet: Pet,
        tasks: list,
        available_minutes: int,
        start_time: str,
    ) -> Schedule:
        """Builds and returns a Schedule by filtering completed tasks, sorting by priority, and fitting tasks within the available time budget."""
        # Convert dicts to Task objects if the caller passed raw form data
        task_objects = [
            Task(**t) if isinstance(t, dict) else t for t in tasks
        ]

        # Skip completed tasks (improvement #3)
        pending = [t for t in task_objects if not t.completed and t.frequency == "daily"]

        # Sort high → medium → low priority (improvement #1)
        pending.sort(key=lambda t: self.PRIORITY_ORDER.get(t.priority, 1))

        # Fit tasks within available time (improvement #2)
        scheduled_tasks: list[ScheduledTask] = []
        time_used = 0
        current_time = start_time

        for task in pending:
            if time_used + task.duration_minutes <= available_minutes:
                end_time = self._advance_time(current_time, task.duration_minutes)
                scheduled_tasks.append(ScheduledTask(
                    task=task,
                    start_time=current_time,
                    end_time=end_time,
                    reason=f"{task.priority.capitalize()} priority — fits within available time",
                ))
                current_time = end_time
                time_used += task.duration_minutes


        scheduled_tasks.sort(
            key=lambda s: datetime.strptime(s.start_time, "%I:%M %p")
        )

        return Schedule(
            owner=owner,
            pet=pet,
            available_minutes=available_minutes,
            scheduled_tasks=scheduled_tasks,
        )

    def sort_by_time(self, scheduled_tasks: list[ScheduledTask]) -> list[ScheduledTask]:
        """Returns the scheduled task list sorted chronologically by start_time."""
        return sorted(
            scheduled_tasks,
            key=lambda s: datetime.strptime(s.start_time, "%I:%M %p")
        )

    def filter_tasks_by_pet(self, pets: list[Pet], pet_name: str) -> list[Task]:
        """Returns all tasks belonging to the pet with the matching name, or an empty list if not found."""
        for pet in pets:
            if pet.name == pet_name:
                return pet.tasks
        return []

    def detect_conflicts(self, scheduled_tasks: list[ScheduledTask]) -> list[str]:
        """Checks every pair of scheduled tasks for overlapping time windows and returns a warning string for each conflict found."""
        warnings = []
        fmt = "%I:%M %p"
        for i in range(len(scheduled_tasks)):
            for j in range(i + 1, len(scheduled_tasks)):
                a = scheduled_tasks[i]
                b = scheduled_tasks[j]
                a_start = datetime.strptime(a.start_time, fmt)
                a_end   = datetime.strptime(a.end_time,   fmt)
                b_start = datetime.strptime(b.start_time, fmt)
                b_end   = datetime.strptime(b.end_time,   fmt)
                if a_start < b_end and b_start < a_end:
                    warnings.append(
                        f"CONFLICT: '{a.task.title}' ({a.start_time}-{a.end_time}) "
                        f"overlaps with '{b.task.title}' ({b.start_time}-{b.end_time})"
                    )
        return warnings

    def reschedule_completed_tasks(self, pet: Pet) -> list[Task]:
        """Finds completed daily or weekly tasks on the pet, adds a fresh next occurrence, and returns the new tasks created."""
        new_tasks = []
        for task in pet.tasks:
            if task.completed and task.frequency in ("daily", "weekly"):
                next_task = task.next_occurrence()
                pet.add_task(next_task)
                new_tasks.append(next_task)
        return new_tasks

    def _advance_time(self, time_str: str, minutes: int) -> str:
        """Parses a 12-hour time string, adds the given minutes, and returns the resulting time as a formatted string."""
        t = datetime.strptime(time_str, "%I:%M %p")
        t += timedelta(minutes=minutes)
        return t.strftime("%I:%M %p")

    def _build_prompt(self, owner: Owner, pet: Pet, tasks: list[Task]) -> str:
        """Constructs the natural-language prompt sent to the AI, embedding the pet's profile, owner name, and full task list with durations and priorities."""
        task_lines = "\n".join(
            f"- {t.title} ({t.duration_minutes} min, {t.priority} priority, "
            f"frequency: {t.frequency}): {t.description}"
            for t in tasks
        )
        return (
            f"Create a daily care schedule for {pet.name}.\n"
            f"Pet info: {pet.summary()}\n"
            f"Owner: {owner.full_name()}\n\n"
            f"Tasks to schedule:\n{task_lines}\n\n"
            "Return a JSON schedule with start/end times and a reason for each task ordering."
        )

    def _parse_response(self, tasks: list[Task], start_time: str, response: dict) -> list[ScheduledTask]:
        """Converts the AI's JSON response into a list of ScheduledTask objects by matching task titles to the original Task instances."""
        scheduled = []
        task_map = {t.title: t for t in tasks}
        for item in response.get("scheduled_tasks", []):
            task = task_map.get(item["title"])
            if task:
                scheduled.append(ScheduledTask(
                    task=task,
                    start_time=item["start_time"],
                    end_time=item["end_time"],
                    reason=item.get("reason", ""),
                ))
        return scheduled
