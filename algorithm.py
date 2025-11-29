# algorithm.py - Different scheduling algorithms

from typing import List, Dict
import config
from scheduler import Task


class SchedulingAlgorithm:
    """Base class for scheduling algorithms"""

    def __init__(self, name: str):
        self.name = name
        self.executed_tasks: List[Task] = []
        self.total_energy = 0.0
        self.total_wait_time = 0.0
        self.total_turnaround_time = 0.0

    def schedule(self, tasks: List[Task]) -> Task:
        """Return next task to execute (must be implemented in subclasses)"""
        raise NotImplementedError

    def execute_task(self, task: Task, current_time: float, power_watts: float) -> None:
        """Record task execution and update metrics"""
        task.start_time = current_time
        task.end_time = current_time + task.duration
        self.executed_tasks.append(task)

        energy_kwh = task.get_energy_consumption(power_watts)
        self.total_energy += energy_kwh
        self.total_wait_time += task.get_wait_time()
        self.total_turnaround_time += task.get_turnaround_time()

    def get_average_wait_time(self) -> float:
        if self.executed_tasks:
            return self.total_wait_time / len(self.executed_tasks)
        return 0.0

    def get_average_turnaround_time(self) -> float:
        if self.executed_tasks:
            return self.total_turnaround_time / len(self.executed_tasks)
        return 0.0

    def get_metrics(self) -> Dict:
        """Return all metrics of this scheduler"""
        return {
            "algorithm": self.name,
            "total_energy_kwh": self.total_energy,
            "tasks_executed": len(self.executed_tasks),
            "avg_wait_time": self.get_average_wait_time(),
            "avg_turnaround_time": self.get_average_turnaround_time(),
            "co2_emissions_kg": self.total_energy * config.EMISSION_FACTOR_KG_CO2_PER_KWH,
        }


class FCFSScheduler(SchedulingAlgorithm):
    """First Come First Served"""

    def __init__(self):
        super().__init__("FCFS")

    def schedule(self, tasks: List[Task]) -> Task:
        if tasks:
            return tasks[0]
        return None


class SJFScheduler(SchedulingAlgorithm):
    """Shortest Job First"""

    def __init__(self):
        super().__init__("SJF")

    def schedule(self, tasks: List[Task]) -> Task:
        if not tasks:
            return None
        return min(tasks, key=lambda t: t.duration)


class PriorityScheduler(SchedulingAlgorithm):
    """Priority Based Scheduling"""

    def __init__(self):
        super().__init__("PriorityBased")

    def schedule(self, tasks: List[Task]) -> Task:
        if not tasks:
            return None
        # Lower priority.value = higher priority
        return min(tasks, key=lambda t: (t.priority.value, t.arrival_time))


class RoundRobinScheduler(SchedulingAlgorithm):
    """Round Robin with time quantum"""

    def __init__(self, time_quantum: int = config.TIME_QUANTUM_MS):
        super().__init__("RoundRobin")
        self.time_quantum = time_quantum

    def schedule(self, tasks: List[Task]) -> Task:
        if tasks:
            return tasks[0]
        return None


class EnergyOptimizedScheduler(SchedulingAlgorithm):
    """Energy-Optimized (Green) Scheduling"""

    def __init__(self):
        super().__init__("EnergyOptimized")

    def schedule(self, tasks: List[Task]) -> Task:
        """
        Green Scheduling Strategy:
        1. Prefer tasks with lower CPU requirements
        2. Tie-break by priority and arrival time
        """
        if not tasks:
            return None

        # First by CPU requirement (lower first), then by priority, then by arrival
        sorted_tasks = sorted(
            tasks,
            key=lambda t: (t.cpu_requirement, t.priority.value, t.arrival_time),
        )
        return sorted_tasks[0]

    def apply_dvfs(self, current_power_watts: float, cpu_usage: float) -> float:
        """
        Dynamic Voltage and Frequency Scaling:
        Reduce power when CPU usage is low.
        """
        if cpu_usage < 30:
            # Low load: reduce to ~60% power
            return current_power_watts * 0.6
        elif cpu_usage < 60:
            # Medium load: reduce to ~80% power
            return current_power_watts * 0.8
        else:
            # High load: full power
            return current_power_watts
