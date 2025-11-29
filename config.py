# Green Scheduling Algorithm Configuration
# System parameters for Mac Silicon
CPU_CORES = 8 # M1/M2/M3 has 8 cores (P-cores + E-cores)
MAX_FREQUENCY_GHZ = 3.2 # Maximum frequency in GHz
BASE_POWER_WATTS = 5.0 # Idle power consumption
MAX_POWER_WATTS = 15.0 # Maximum power consumption
MEMORY_GB = 16 # System RAM
# Task simulation parameters
NUM_TASKS = 20 # Number of tasks to schedule
TASK_DURATION_MIN = 0.5 # Min task duration (seconds)
TASK_DURATION_MAX = 5.0 # Max task duration (seconds)
TASK_PRIORITY_LEVELS = 3 # High, Medium, Low
# Energy conversion factors (India)
EMISSION_FACTOR_KG_CO2_PER_KWH = 0.73 # kg CO2 per kWh in India
POWER_COST_PER_KWH = 8.0 # ₹ per kWh (approximate)
# Scheduling algorithms to compare
ALGORITHMS = ['FCFS', 'SJF', 'RoundRobin', 'PriorityBased', 'EnergyOptimized']
# Time quantum for Round Robin (milliseconds)
TIME_QUANTUM_MS = 100
# Simulation parameters
SIMULATION_TIME = 60 # Total simulation time (seconds)
SAMPLING_INTERVAL = 1 # Collect data every N seconds
# Output settings
ENABLE_LOGGING = True
ENABLE_VISUALIZATION = True
SAVE_RESULTS = True
