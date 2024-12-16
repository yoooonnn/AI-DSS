# simulator/run.py

import schedule
import timeit
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
    device_types = ['Light', 'Speaker']

    # Set the number of devices to add per user (1 Light and 1 Speaker)
    logging.info("Adding 1 Light and 1 Smart Speaker for each user...")

    # Add Light and Smart Speaker devices for each user
    simulator.add_device('Light', user1_id)
    simulator.add_device('Speaker', user1_id)

    simulator.add_device('Light', user2_id)
    simulator.add_device('Speaker', user2_id)

    simulator.add_device('Light', user3_id)
    simulator.add_device('Speaker', user3_id)

    # Run simulation
    start_time = datetime.now()
    logging.info(f"Starting simulation at: {start_time}")
    simulator.simulate(start_time, duration_hours=0.1)

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