import random
from datetime import timedelta

# Washing Machine device class with enhanced actions (without spinDry)
class WashingMachine:
    def __init__(self, device_id, user_id):
        self.device_id = device_id
        self.user_id = user_id
        self.state = {
            'status': 'off',  # Initial status is off
            'wash_mode': 'normal',  # Default wash mode is normal
            'progress': 0  # Progress (0% to 100%)
        }

    def generate_action(self, current_time):
        # Possible actions to change
        actions = ['status', 'wash_mode', 'progress']
        
        # Randomly select an action
        action = random.choices(actions, [0.4, 0.3, 0.3])[0]  # Assign weights to actions
        
        # Initialize function to ensure it is always set
        function = None
        
        # Generate new value based on selected action
        if action == 'status':
            # Randomly choose between 'off', 'washing', or 'spinning'
            new_value = random.choice(['off', 'washing'])
            function = 'startWash' if new_value == 'washing' else 'stopWash'
        
        elif action == 'wash_mode':
            # Choose a new wash mode (quickWash, delicate, heavyDuty, etc.)
            new_value = random.choice(['quickWash', 'delicate', 'heavyDuty', 'normal'])
            function = 'setWashMode'
        
        elif action == 'progress':
            # Progress could be randomly updated between 0% and 100%
            new_value = random.randint(0, 100)
            function = 'checkWashProgress'
        
        # Update the state with the new value
        self.state[action] = new_value

        # Return the action details along with the updated state and function
        return {
            'device_id': self.device_id,
            'user_id': self.user_id,
            'action': action,
            'value': new_value,
            'function': function,  # The function to trigger (startWash, setWashMode, checkWashProgress)
            'timestamp': current_time,
            'state': self.state  # Current state of the washing machine (including the mode and progress)
        }
