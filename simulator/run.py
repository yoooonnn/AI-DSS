import os
import sys
from datetime import datetime

# Add the current directory to the system path for importing modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

# Import the SmartHomeSimulator class from the simulator module
from simulator import SmartHomeSimulator

# Initialize the simulator
simulator = SmartHomeSimulator()

# Add users
simulator.users = {
    1: 'Office Worker',  # User 1: Office worker
    2: 'Remote Worker',  # User 2: Remote worker
    3: 'Student'         # User 3: Student
}

# Add devices
simulator.add_device(1, 'light', 1)  # Office worker's light
simulator.add_device(2, 'light', 2)  # Remote worker's light
# ... Add more devices as needed

# Run the simulation
start_time = datetime.now()  # Start time for the simulation (current time)
simulator.simulate(start_time, duration_hours=24)  # Simulate for 24 hours

# Save the results
for log in simulator.logs:
    # Code to save the log to a database (e.g., SQLite, PostgreSQL, etc.)
    pass
