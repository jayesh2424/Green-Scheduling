# visualization.py - Create graphs and charts

import os
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd


class DataVisualizer:
    """Create visualizations for energy and performance analysis"""

    def __init__(self):
        self.output_dir = "results"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def plot_energy_comparison(self, results: Dict) -> None:
        """Bar chart comparing energy consumption of each algorithm"""
        algorithms = list(results.keys())
        energy_values = [results[algo]["total_energy_kwh"] for algo in algorithms]

        plt.figure(figsize=(10, 6))
        bars = plt.bar(
            algorithms,
            energy_values,
            color="#2ecc71",
            edgecolor="black",
            linewidth=1.5,
        )

        # Add labels on bars
        for bar, value in zip(bars, energy_values):
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{value:.6f}",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
            )

        plt.title("Energy Consumption by Scheduling Algorithm", fontsize=14, fontweight="bold")
        plt.xlabel("Algorithm", fontsize=12)
        plt.ylabel("Energy (kWh)", fontsize=12)
        plt.xticks(rotation=45, ha="right")
        plt.grid(axis="y", alpha=0.3)
        plt.tight_layout()

        filename = f"{self.output_dir}/01_energy_comparison.png"
        plt.savefig(filename, dpi=300, bbox_inches="tight")
        print(f"✓ Saved: {filename}")
        plt.close()

    def plot_co2_comparison(self, results: Dict) -> None:
        """Bar chart comparing CO₂ emissions of each algorithm"""
        algorithms = list(results.keys())
        co2_values = [results[algo]["co2_emissions_kg"] for algo in algorithms]

        plt.figure(figsize=(10, 6))
        bars = plt.bar(
            algorithms,
            co2_values,
            color="#e74c3c",
            edgecolor="black",
            linewidth=1.5,
        )

        for bar, value in zip(bars, co2_values):
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{value:.4f}",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
            )

        plt.title("CO₂ Emissions by Scheduling Algorithm", fontsize=14, fontweight="bold")
        plt.xlabel("Algorithm", fontsize=12)
        plt.ylabel("CO₂ (kg CO₂e)", fontsize=12)
        plt.xticks(rotation=45, ha="right")
        plt.grid(axis="y", alpha=0.3)
        plt.tight_layout()

        filename = f"{self.output_dir}/02_co2_comparison.png"
        plt.savefig(filename, dpi=300, bbox_inches="tight")
        print(f"✓ Saved: {filename}")
        plt.close()

    def plot_performance_metrics(self, results: Dict) -> None:
        """Side-by-side charts for avg wait and turnaround time"""
        algorithms = list(results.keys())

        data = {
            "Algorithm": algorithms,
            "Avg Wait Time (s)": [results[algo]["avg_wait_time"] for algo in algorithms],
            "Avg Turnaround (s)": [results[algo]["avg_turnaround_time"] for algo in algorithms],
        }

        df = pd.DataFrame(data)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        # Average wait time
        ax1.bar(df["Algorithm"], df["Avg Wait Time (s)"], color="#3498db", edgecolor="black")
        ax1.set_title("Average Wait Time", fontsize=12, fontweight="bold")
        ax1.set_ylabel("Time (seconds)", fontsize=11)
        ax1.tick_params(axis="x", rotation=45)
        ax1.grid(axis="y", alpha=0.3)

        # Average turnaround time
        ax2.bar(df["Algorithm"], df["Avg Turnaround (s)"], color="#9b59b6", edgecolor="black")
        ax2.set_title("Average Turnaround Time", fontsize=12, fontweight="bold")
        ax2.set_ylabel("Time (seconds)", fontsize=11)
        ax2.tick_params(axis="x", rotation=45)
        ax2.grid(axis="y", alpha=0.3)

        plt.tight_layout()
        filename = f"{self.output_dir}/03_performance_metrics.png"
        plt.savefig(filename, dpi=300, bbox_inches="tight")
        print(f"✓ Saved: {filename}")
        plt.close()

    def create_summary_table(self, results: Dict) -> pd.DataFrame:
        """Create and save a CSV summary of all metrics"""
        df = pd.DataFrame(results).T
        df = df.round(6)

        csv_filename = f"{self.output_dir}/04_results_summary.csv"
        df.to_csv(csv_filename)
        print(f"✓ Saved: {csv_filename}")

        print("\n" + "=" * 80)
        print("COMPLETE RESULTS SUMMARY")
        print("=" * 80)
        print(df.to_string())
        print("=" * 80 + "\n")

        return df

    def generate_all_visualizations(self, results: Dict) -> None:
        """Generate all charts and summary files"""
        print("\n" + "=" * 60)
        print("GENERATING VISUALIZATIONS")
        print("=" * 60 + "\n")

        self.plot_energy_comparison(results)
        self.plot_co2_comparison(results)
        self.plot_performance_metrics(results)
        self.create_summary_table(results)

        print("\n✓ All visualizations completed!")
        print(f"✓ Results saved to: {os.path.abspath(self.output_dir)}")
