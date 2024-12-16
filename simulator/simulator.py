# simulatr/simulator.py

from datetime import datetime, timedelta
import random
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from devices.light import Light
from devices.robot_vacuum import RobotVacuum
from devices.washing_machine import WashingMachine
from devices.air_conditioner import AirConditioner
from utils.user_pattern import user_patterns

# SmartHomeSimulator class that handles the simulation logic
class SmartHomeSimulator:
    def __init__(self):
        self.devices = {}  # device_id : device_instance mapping
        self.users = {}    # user_id : user_type mapping
        self.logs = []  # List of simulation logs

    def add_user(self, user_type):
        user_id = ''.join(random.choices('0123456789abcdef', k=130))
        self.users[user_id] = user_type
        print(f"User added: {user_id} ({user_type})")
        return user_id
    
    def add_device(self, device_type, user_id):
        device_id = ''.join(random.choices('0123456789abcdef', k=130))
        if device_type == 'light':
            self.devices[device_id] = Light(device_id, user_id)  # Add a light device
        elif device_type == 'robot_vacuum':
            self.devices[device_id] = RobotVacuum(device_id, user_id)
        elif device_type == 'washing_machine':
            self.devices[device_id] = WashingMachine(device_id, user_id)
        elif device_type == 'air_conditioner':
            self.devices[device_id] = AirConditioner(device_id, user_id)

    def simulate(self, start_time, duration_hours):
        current_time = start_time
        end_time = start_time + timedelta(hours=duration_hours)
        
        # Run the simulation for the given duration
        while current_time < end_time:
            for device in self.devices.values():
                # Generate actions for each device based on the current time
                interaction = device.generate_action(current_time)
                self.logs.append(interaction)
            
            # Move forward in time by a random amount (1 to 5 minutes)
            current_time += timedelta(minutes=random.randint(1, 5))

        # Save all generated logs to the database
        # self.save_logs_to_db()

    # def save_logs_to_db(self):
    #     # Save each log entry to the database
    #     for log in self.logs:
    #         simulation_log = SimulationLog(
    #             device_id=log['device_id'],
    #             user_id=log['user_id'],
    #             action=log['action'],
    #             value=log['value'],
    #             timestamp=log['timestamp']
    #         )
    #         db.session.add(simulation_log)  # Add log to session
    #     db.session.commit()  # Commit session to the database
            
    def _should_interact(self, time, user_type):
        pattern = user_patterns[user_type]
        
        # 활성 시간대 체크
        is_active_hour = any(start <= time.hour < end 
                           for start, end in pattern['active_hours'])
        
        # 요일별 확률 적용
        is_weekday = time.weekday() < 5
        prob = pattern['interaction_probability']['weekday' if is_weekday else 'weekend']
        
        return is_active_hour and random.random() < prob