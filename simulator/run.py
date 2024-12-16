# simulator/run.py

import os
import sys
import random
from datetime import datetime
import logging

# Add current directory to system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

# Import simulator and log handler
from simulator import SmartHomeSimulator
from log_api_handler import handle_log

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def run_simulation():
    # Initialize simulator
    logging.info("Initializing Smart Home Simulator...")
    simulator = SmartHomeSimulator()

    # Add users
    logging.info("Adding users...")
    user1_id = simulator.add_user('Office Worker')
    user2_id = simulator.add_user('Remote Worker')
    user3_id = simulator.add_user('Student')

    # Available device types
    device_types = ['light', 'robot_vacuum', 'washing_machine', 'air_conditioner']

    # Set random number of devices per user
    logging.info("Adding random devices for each user...")
    num_devices_user1 = random.randint(1, 4)
    num_devices_user2 = random.randint(1, 4)
    num_devices_user3 = random.randint(1, 4)

    # Add devices for each user
    for _ in range(num_devices_user1):
        simulator.add_device(random.choice(device_types), user1_id)
    for _ in range(num_devices_user2):
        simulator.add_device(random.choice(device_types), user2_id)
    for _ in range(num_devices_user3):
        simulator.add_device(random.choice(device_types), user3_id)

    # Run simulation
    start_time = datetime.now()
    logging.info(f"Starting simulation at: {start_time}")
    simulator.simulate(start_time, duration_hours=24)

    # Send logs to backend
    logging.info("Simulation completed. Sending logs to backend...")
    handle_log(simulator.logs)

if __name__ == "__main__":
    try:
        run_simulation()
        logging.info("Simulation and log transmission completed successfully")
    except Exception as e:
        logging.error(f"Error during simulation: {str(e)}")
        sys.exit(1)