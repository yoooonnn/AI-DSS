import random
from datetime import datetime, timedelta

# Robot Vacuum device class with scheduling
class RobotVacuum:
    def __init__(self, device_id, user_id):
        self.device_id = device_id
        self.user_id = user_id
        self.state = {
            'status': 'idle',  # Default status is 'idle'
            'mode': 'normal',  # Default mode is 'normal'
            'schedule': None   # No schedule by default
        }
        
        # Default schedule (empty, no cleaning)
        self.schedule = None

    def generate_action(self, current_time):
        # Possible actions to change
        actions = ['status', 'mode', 'schedule']
        
        # Choose an action (status, mode, or schedule change)
        action = random.choices(actions, [0.6, 0.3, 0.1])[0]  # Higher probability for status and mode
        
        # Initialize function variable to ensure it's always defined
        function = None
        
        # Generate new value based on the selected action
        if action == 'status':
            new_value = random.choice(['idle', 'cleaning', 'charging'])
            if new_value == 'cleaning':
                function = 'startCleaning'
            elif new_value == 'idle':
                function = 'stopCleaning'
            elif new_value == 'charging':
                function = 'charge'
        
        elif action == 'mode':
            new_value = random.choice(['normal', 'deepCleaning', 'spotCleaning'])
            function = 'setMode'
        
        elif action == 'schedule':
            # Define a schedule: Randomly choose a start and stop time for cleaning
            start_time = current_time + timedelta(minutes=random.randint(30, 60))  # Start in 30 to 60 minutes
            stop_time = start_time + timedelta(minutes=random.randint(30, 120))  # Cleaning duration: 30 to 120 minutes
            self.schedule = {'start': start_time, 'stop': stop_time}
            new_value = f'Schedule set: {start_time.strftime("%Y-%m-%d %H:%M:%S")} to {stop_time.strftime("%Y-%m-%d %H:%M:%S")}'
            function = 'setSchedule'

        # Update the state with the new value
        self.state[action] = new_value
        
        # Return the action details along with the updated state and function
        return {
            'device_id': self.device_id,
            'user_id': self.user_id,
            'action': action,
            'value': new_value,
            'function': function,  # Function to trigger (startCleaning, setMode, setSchedule)
            'timestamp': current_time,
            'state': self.state  # Current state of the robot vacuum (including the schedule)
        }

