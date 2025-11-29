# simulation.py - Run scheduling simulations

import random
from typing import List, Dict

import config
from scheduler import Task, TaskPriority
from algorithm import (
    FCFSScheduler,
    SJFScheduler,
    PriorityScheduler,
    RoundRobinScheduler,
    EnergyOptimizedScheduler,
)
from energy_monitor import EnergyMonitor
import json


class Simulator:
    """Main simulation engine"""

    def __init__(self):
        self.tasks: List[Task] = []
        self.schedulers: Dict[str, object] = {}
        self.monitors: Dict[str, EnergyMonitor] = {}
        self.results: Dict[str, Dict] = {}

    def generate_random_tasks(self, num_tasks: int = config.NUM_TASKS) -> List[Task]:
        """Generate random tasks for simulation"""
        self.tasks = []

        for _ in range(num_tasks):
            task = Task(
                duration=random.uniform(config.TASK_DURATION_MIN, config.TASK_DURATION_MAX),
                priority=random.choice(list(TaskPriority)),
                arrival_time=random.uniform(0, config.SIMULATION_TIME / 2),
                cpu_requirement=random.uniform(10, 100),
            )
            self.tasks.append(task)

        # Sort by arrival time
        self.tasks.sort(key=lambda t: t.arrival_time)
        print(f"Generated {num_tasks} tasks")
        return self.tasks

    def initialize_schedulers(self) -> None:
        """Initialize all scheduling algorithms"""
        self.schedulers = {
            "FCFS": FCFSScheduler(),
            "SJF": SJFScheduler(),
            "PriorityBased": PriorityScheduler(),
            "RoundRobin": RoundRobinScheduler(),
            "EnergyOptimized": EnergyOptimizedScheduler(),
        }
        print(f"Initialized {len(self.schedulers)} schedulers")

    def run_simulation_for_algorithm(self, algorithm_name: str, tasks: List[Task]) -> Dict:
        """Run simulation for a specific algorithm"""
        scheduler = self.schedulers[algorithm_name]
        monitor = EnergyMonitor()

        # Make a shallow copy of tasks list
        remaining_tasks: List[Task] = [t for t in tasks]
        current_time = 0.0

        while remaining_tasks and current_time < config.SIMULATION_TIME:
            # Get next task to execute
            next_task = scheduler.schedule(remaining_tasks)

            if next_task:
                # Compute power based on this task's CPU requirement
                power_watts = monitor.calculate_power_watts(next_task.cpu_requirement)

                # Execute task (update metrics)
                scheduler.execute_task(next_task, current_time, power_watts)

                # Record a reading (simplified: use task's CPU requirement as usage)
                monitor.record_reading(
                    cpu_usage=next_task.cpu_requirement,
                    memory_usage=30.0,  # dummy memory usage
                    power_watts=power_watts,
                )

                # Update time and remove task from queue
                current_time += next_task.duration
                remaining_tasks.remove(next_task)
            else:
                # No task available, advance time slightly
                current_time += 0.1

        # Store references
        self.schedulers[algorithm_name] = scheduler
        self.monitors[algorithm_name] = monitor

        return scheduler.get_metrics()

    def run_all_simulations(self) -> Dict[str, Dict]:
        """Run simulations for all algorithms"""
        print("\n" + "=" * 60)
        print("STARTING SIMULATIONS")
        print("=" * 60)

        self.initialize_schedulers()

        for algorithm_name in config.ALGORITHMS:
            print(f"\nRunning {algorithm_name}...")
            metrics = self.run_simulation_for_algorithm(algorithm_name, self.tasks)
            self.results[algorithm_name] = metrics
            print(f"✓ {algorithm_name} completed")
            print(f"  Energy: {metrics['total_energy_kwh']:.6f} kWh")
            print(f"  CO₂:    {metrics['co2_emissions_kg']:.4f} kg")

        return self.results

    def compare_algorithms(self):
        """Compare all algorithms and print ranking"""
        print("\n" + "=" * 60)
        print("ALGORITHM COMPARISON")
        print("=" * 60)

        # Sort by energy
        sorted_by_energy = sorted(
            self.results.items(),
            key=lambda x: x[1]["total_energy_kwh"],
        )
        # Sort by CO2
        sorted_by_co2 = sorted(
            self.results.items(),
            key=lambda x: x[1]["co2_emissions_kg"],
        )

        print("\nEnergy Consumption Ranking:")
        for i, (algo, metrics) in enumerate(sorted_by_energy, start=1):
            print(f"  {i}. {algo}: {metrics['total_energy_kwh']:.6f} kWh")

        print("\nCO₂ Emissions Ranking:")
        for i, (algo, metrics) in enumerate(sorted_by_co2, start=1):
            print(f"  {i}. {algo}: {metrics['co2_emissions_kg']:.4f} kg")

        best_energy_algo = sorted_by_energy[0][0]
        best_co2_algo = sorted_by_co2[0][0]

        print(f"\n✓ Best Energy Algorithm: {best_energy_algo}")
        print(f"✓ Best CO₂ Reduction:    {best_co2_algo}")

        return best_energy_algo, best_co2_algo

    def save_results(self, filename: str = "results/simulation_results.json") -> None:
        """Save results to JSON file"""
        with open(filename, "w") as f:
            json.dump(self.results, f, indent=2)
        print(f"\n✓ Results saved to {filename}")
