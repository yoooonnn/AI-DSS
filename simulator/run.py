# simulator/run.py

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
user1_id = simulator.add_user('Office Worker')  # User 1: Office Worker
user2_id = simulator.add_user('Remote Worker')  # User 2: Remote Worker
user3_id = simulator.add_user('Student')  # User 3: Student

# Add devices
simulator.add_device('light', user1_id)  # Office worker's light
simulator.add_device('light', user2_id)  # Remote worker's light
# ... Add more devices as needed

# Run the simulation
start_time = datetime.now()  # Start time for the simulation (current time)
simulator.simulate(start_time, duration_hours=24)  # Simulate for 24 hours

# Save the results
for log in simulator.logs:
    # Code to save the log to a database (e.g., SQLite, PostgreSQL, etc.)
    pass
