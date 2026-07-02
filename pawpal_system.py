from dataclasses import dataclass, field


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
        return sum(st.task.duration_minutes for st in self.scheduled_tasks)

    def display(self) -> str:
        """Renders the full schedule as a formatted multi-line string with a header, per-task lines, and an optional AI-generated summary."""
        header = (
            f"Schedule for {self.pet.name} "
            f"(owner: {self.owner.full_name()})\n"
            f"Available: {self.available_minutes} min | "
            f"Scheduled: {self.total_duration()} min\n"
            + "-" * 50
        )
        task_lines = "\n".join(st.display() for st in self.scheduled_tasks)
        footer = f"\nSummary: {self.summary}" if self.summary else ""
        return f"{header}\n{task_lines}{footer}"


class Scheduler:
    def generate_schedule(
        self,
        owner: Owner,
        pet: Pet,
        _tasks: list[Task],
        available_minutes: int,
        _start_time: str,
    ) -> Schedule:
        """Builds and returns a Schedule for the given owner and pet by selecting and ordering tasks within the available time budget using AI."""
        # TODO: wire up AI — call self._build_prompt(owner, pet, _tasks),
        # pass result to ai_client.complete(), then self._parse_response(_tasks, _start_time, response)
        scheduled_tasks: list[ScheduledTask] = []
        return Schedule(
            owner=owner,
            pet=pet,
            available_minutes=available_minutes,
            scheduled_tasks=scheduled_tasks,
        )

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
