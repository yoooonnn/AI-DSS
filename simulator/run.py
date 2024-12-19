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

    # Define diverse user profiles
    user_profiles = [
        'Office Worker',          # 9-5 traditional work schedule
        'Remote Worker',          # Works from home
        'Student',               # College/University student
        'Stay-at-home Parent',   # At home during day with different schedule
        'Night Shift Worker',    # Inverse schedule
        'Elderly Resident',      # More time at home, regular schedule
        'Freelancer',           # Flexible schedule
        'Weekend Traveler',     # Regular weekday, traveling weekends
        'Family with Kids',     # Complex schedule with multiple routines
        'Fitness Enthusiast'    # Early morning/evening activity peaks
    ]

    # Add users
    logging.info("Adding users...")
    user_ids = {}
    for profile in user_profiles:
        user_ids[profile] = simulator.add_user(profile)
        logging.info(f"Added user: {profile}")

    # Available device types
    device_types = ['Light', 'Speaker']

    # Add devices for each user based on their profile
    logging.info("Adding devices for each user profile...")
    
    # Office Worker - basic setup
    simulator.add_device('Light', user_ids['Office Worker'])
    simulator.add_device('Speaker', user_ids['Office Worker'])
    
    # Remote Worker - more devices since always at home
    simulator.add_device('Light', user_ids['Remote Worker'])
    simulator.add_device('Light', user_ids['Remote Worker'])
    simulator.add_device('Speaker', user_ids['Remote Worker'])
    
    # Student - multiple lights for study areas
    simulator.add_device('Light', user_ids['Student'])
    simulator.add_device('Light', user_ids['Student'])
    simulator.add_device('Speaker', user_ids['Student'])
    
    # Stay-at-home Parent - multiple devices throughout house
    simulator.add_device('Light', user_ids['Stay-at-home Parent'])
    simulator.add_device('Light', user_ids['Stay-at-home Parent'])
    simulator.add_device('Speaker', user_ids['Stay-at-home Parent'])
    simulator.add_device('Speaker', user_ids['Stay-at-home Parent'])
    
    # Night Shift Worker - emphasis on lighting
    simulator.add_device('Light', user_ids['Night Shift Worker'])
    simulator.add_device('Light', user_ids['Night Shift Worker'])
    simulator.add_device('Speaker', user_ids['Night Shift Worker'])
    
    # Elderly Resident - simple setup with multiple lights
    simulator.add_device('Light', user_ids['Elderly Resident'])
    simulator.add_device('Light', user_ids['Elderly Resident'])
    simulator.add_device('Speaker', user_ids['Elderly Resident'])
    
    # Freelancer - flexible setup
    simulator.add_device('Light', user_ids['Freelancer'])
    simulator.add_device('Speaker', user_ids['Freelancer'])
    
    # Weekend Traveler - basic setup
    simulator.add_device('Light', user_ids['Weekend Traveler'])
    simulator.add_device('Speaker', user_ids['Weekend Traveler'])
    
    # Family with Kids - multiple devices throughout
    simulator.add_device('Light', user_ids['Family with Kids'])
    simulator.add_device('Light', user_ids['Family with Kids'])
    simulator.add_device('Light', user_ids['Family with Kids'])
    simulator.add_device('Speaker', user_ids['Family with Kids'])
    simulator.add_device('Speaker', user_ids['Family with Kids'])
    
    # Fitness Enthusiast - basic setup
    simulator.add_device('Light', user_ids['Fitness Enthusiast'])
    simulator.add_device('Speaker', user_ids['Fitness Enthusiast'])

    # Run simulation
    start_time = datetime.now()
    logging.info(f"Starting simulation at: {start_time}")
    simulator.simulate(start_time, duration_hours=168)

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