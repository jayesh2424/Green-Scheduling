#!/usr/bin/env python3
# main.py - Main execution script for Green Scheduling Algorithm

import sys
import time

from simulation import Simulator
from visualization import DataVisualizer


def print_banner() -> None:
    """Print welcome banner"""
    banner = """
╔════════════════════════════════════════════════════════════╗
║        GREEN SCHEDULING ALGORITHM SIMULATOR                ║
║     Energy-Efficient Task Scheduling for Mac Silicon       ║
╚════════════════════════════════════════════════════════════╝
"""
    print(banner)


def main() -> int:
    """Main execution function"""
    print_banner()

    try:
        # Step 1: Initialize simulator
        print("Step 1: Initializing simulator...")
        simulator = Simulator()
        print("✓ Simulator initialized\n")

        # Step 2: Generate tasks
        print("Step 2: Generating random tasks...")
        simulator.generate_random_tasks()
        print("✓ Tasks generated\n")

        # Step 3: Run simulations
        print("Step 3: Running simulations (this may take 30-60 seconds)...")
        start_time = time.time()
        results = simulator.run_all_simulations()
        elapsed_time = time.time() - start_time
        print(f"✓ Simulations completed in {elapsed_time:.2f} seconds\n")

        # Step 4: Compare algorithms
        print("Step 4: Comparing algorithms...")
        best_energy, best_co2 = simulator.compare_algorithms()

        # Step 5: Visualize results
        print("\nStep 5: Creating visualizations...")
        visualizer = DataVisualizer()
        visualizer.generate_all_visualizations(results)

        # Step 6: Save results
        print("\nStep 6: Saving results...")
        simulator.save_results()

        print("\n" + "=" * 60)
        print("✓ SIMULATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nNext Steps:")
        print("Enjoy! This was a successful hunch")
        return 0

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
