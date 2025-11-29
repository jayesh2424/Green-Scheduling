# scheduler.py - Task and Scheduler classes
import time
import uuid
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
import config


class TaskPriority(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3


@dataclass
class Task:
    """Represents a single task to be scheduled"""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    duration: float = 0.0          # Duration in seconds
    priority: TaskPriority = TaskPriority.MEDIUM
    arrival_time: float = 0.0      # When task arrives
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    cpu_requirement: float = 50.0  # CPU percentage needed (0-100)
    memory_requirement: float = 256.0  # Memory in MB

    def __post_init__(self):
        self.created_at = time.time()

    def get_wait_time(self) -> float:
        """Calculate how long task waited before execution"""
        if self.start_time is not None:
            return self.start_time - self.arrival_time
        return 0.0

    def get_turnaround_time(self) -> float:
        """Calculate total time from arrival to completion"""
        if self.end_time is not None:
            return self.end_time - self.arrival_time
        return 0.0

    def get_energy_consumption(self, power_watts: float) -> float:
        """Calculate energy used by this task in kWh"""
        energy_joules = power_watts * self.duration      # Power * Time
        energy_kwh = energy_joules / (3600 * 1000)       # Convert to kWh
        return energy_kwh

    def __repr__(self) -> str:
        # Nice printable representation of a Task
        return f"Task({self.task_id}, dur={self.duration:.2f}s, priority={self.priority.name})"


class TaskQueue:
    """Manages a queue of tasks"""

    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to the queue"""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the queue"""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Retrieve a specific task by ID"""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def get_next_task(self, algorithm: str) -> Optional[Task]:
        """Get next task based on scheduling algorithm"""
        if not self.tasks:
            return None

        if algorithm == 'FCFS':
            # First task that arrived
            return self.tasks[0]

        elif algorithm == 'SJF':
            # Return shortest task
            return min(self.tasks, key=lambda t: t.duration)

        elif algorithm == 'PriorityBased':
            # Return highest priority task (lowest priority value)
            return min(self.tasks, key=lambda t: (t.priority.value, t.arrival_time))

        elif algorithm == 'EnergyOptimized':
            # Return task with lowest energy requirement (CPU requirement)
            return min(self.tasks, key=lambda t: t.cpu_requirement)

        # Default: FCFS
        return self.tasks[0]

    def is_empty(self) -> bool:
        """Check if queue is empty"""
        return len(self.tasks) == 0

    def __len__(self) -> int:
        return len(self.tasks)

    def __repr__(self) -> str:
        return f"TaskQueue(size={len(self.tasks)})"
