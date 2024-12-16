import os
import sys
from datetime import datetime
import logging
import random

# Add the current directory to the system path for importing modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from simulator import SmartHomeSimulator

# 설정: 로깅 활성화
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Test 시뮬레이터 동작 확인용 코드
def test_simulator():
    # 시뮬레이터 초기화
    simulator = SmartHomeSimulator()

    # Add users
    user1_id = simulator.add_user('Office Worker')  # User 1: Office Worker
    user2_id = simulator.add_user('Remote Worker')  # User 2: Remote Worker
    user3_id = simulator.add_user('Student')  # User 3: Student

    # Add random devices to each user
    device_types = ['light', 'robot_vacuum', 'washing_machine', 'air_conditioner']
    
    num_devices_user1 = random.randint(1, 4)
    num_devices_user2 = random.randint(1, 4)
    num_devices_user3 = random.randint(1, 4)

    for _ in range(num_devices_user1):
        simulator.add_device(random.choice(device_types), user1_id)  # User 1 gets a random device
    for _ in range(num_devices_user2):
        simulator.add_device(random.choice(device_types), user2_id)  # User 2 gets a random device
    for _ in range(num_devices_user3):
        simulator.add_device(random.choice(device_types), user3_id)  # User 3 gets a random device

    # Run the simulation
    start_time = datetime.now()  # Start time for the simulation (current time)
    simulator.simulate(start_time, duration_hours=24)  # Simulate for 24 hours

# 시뮬레이션 로그 출력
    logging.info("Simulation finished. Logs:")
    
    # 로그 출력 형식 개선
    for log in simulator.logs:
        device_type = log['device_type']
        device_id = log['device_id']
        user_id = log['user_id']
        action = log['action']
        value = log['value']
        timestamp = log['timestamp']
        state = log['state']  # Include the current state of the device
        function = log['function'] 

        # Print out the log in a readable way
        logging.info(f"Device: {device_type} (User: {user_id})")
        logging.info(f"  Action: {action} -> Function: {function}")
        logging.info(f"  Value: {value}")
        logging.info(f"  Timestamp: {timestamp}")
        logging.info(f"  Current State: {state}")
        logging.info("-" * 50)  # Separating logs for readability


if __name__ == "__main__":
    test_simulator()
