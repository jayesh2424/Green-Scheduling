# energy_monitor.py - Monitor system energy consumption

import psutil
import config
from datetime import datetime


class EnergyMonitor:
    """Monitor and calculate energy consumption"""

    def __init__(self):
        self.readings = []
        self.start_time = datetime.now()
        self.total_energy_kwh = 0.0
        self.total_co2_kg = 0.0
        self.total_cost_inr = 0.0

    def get_cpu_usage(self) -> float:
        """Get current CPU usage percentage"""
        return psutil.cpu_percent(interval=0.1)

    def get_memory_usage(self) -> float:
        """Get current memory usage percentage"""
        return psutil.virtual_memory().percent

    def get_cpu_freq_ghz(self) -> float:
        """Get current CPU frequency in GHz"""
        try:
            freq = psutil.cpu_freq()
            if freq:
                return freq.current / 1000.0  # MHz -> GHz
        except Exception:
            return config.MAX_FREQUENCY_GHZ
        return config.MAX_FREQUENCY_GHZ

    def calculate_power_watts(self, cpu_usage_percent: float) -> float:
        """
        Calculate power consumption based on CPU usage.

        Linear model:
        Power = Base + (Max - Base) * (CPU% / 100)
        """
        power = (
            config.BASE_POWER_WATTS
            + (config.MAX_POWER_WATTS - config.BASE_POWER_WATTS) * (cpu_usage_percent / 100.0)
        )
        return power

    def calculate_co2_emissions(self, energy_kwh: float) -> float:
        """Calculate CO₂ emissions (kg CO₂e) from energy in kWh"""
        return energy_kwh * config.EMISSION_FACTOR_KG_CO2_PER_KWH

    def calculate_energy_cost(self, energy_kwh: float) -> float:
        """Calculate cost of energy consumed in INR"""
        return energy_kwh * config.POWER_COST_PER_KWH

    def record_reading(self, cpu_usage: float, memory_usage: float, power_watts: float) -> None:
        """Record a snapshot of system metrics"""
        reading = {
            "timestamp": datetime.now(),
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "power_watts": power_watts,
        }
        self.readings.append(reading)

    def get_total_energy_kwh(self) -> float:
        """Calculate total energy consumption (kWh) from all readings"""
        total_joules = 0.0

        # Need at least 2 readings to integrate over time
        for i in range(len(self.readings) - 1):
            current = self.readings[i]
            next_reading = self.readings[i + 1]

            # Time elapsed between readings in seconds
            time_delta = (next_reading["timestamp"] - current["timestamp"]).total_seconds()

            # Energy (Joules) = Power (Watts) * Time (seconds)
            energy_joules = current["power_watts"] * time_delta
            total_joules += energy_joules

        # Convert Joules to kWh (1 kWh = 3,600,000 J)
        self.total_energy_kwh = total_joules / 3_600_000.0
        return self.total_energy_kwh

    def get_total_co2_kg(self) -> float:
        """Calculate total CO₂ emissions (kg CO₂e)"""
        energy_kwh = self.get_total_energy_kwh()
        self.total_co2_kg = self.calculate_co2_emissions(energy_kwh)
        return self.total_co2_kg

    def get_total_cost_inr(self) -> float:
        """Calculate total energy cost in INR"""
        energy_kwh = self.get_total_energy_kwh()
        self.total_cost_inr = self.calculate_energy_cost(energy_kwh)
        return self.total_cost_inr

    def print_summary(self) -> None:
        """Print energy consumption summary to console"""
        print("\n" + "=" * 60)
        print("ENERGY CONSUMPTION SUMMARY")
        print("=" * 60)
        print(f"Total Energy:    {self.get_total_energy_kwh():.6f} kWh")
        print(f"CO₂ Emissions:   {self.get_total_co2_kg():.4f} kg CO₂e")
        print(f"Cost:            ₹{self.get_total_cost_inr():.2f}")
        print(f"Number of readings: {len(self.readings)}")
        print("=" * 60 + "\n")
