import random

# Air Conditioner device class
class AirConditioner:
    def __init__(self, device_id, user_id):
        self.device_id = device_id
        self.user_id = user_id  # User ID associated with this device
        self.state = {
            'power': 'off',           # State: Air conditioner power (on/off)
            'temperature': 22,        # Current temperature (default 22°C)
            'fanSpeed': 'medium',     # Fan speed (low, medium, high)
            'mode': 'cooling'         # Mode (cooling, heating, fan-only)
        }

    def generate_action(self, current_time):
        # Possible actions to change
        actions = ['power', 'temperature', 'fanSpeed', 'mode']
        
        # Choose an action based on weighted probabilities
        action = random.choices(actions, [0.3, 0.2, 0.2, 0.3])[0]  # Action selection with weight distribution
        
        # Define new values based on the selected action
        if action == 'power':
            # Toggle power on/off
            if self.state['power'] == 'off':
                new_value = 'on'  # Power turned on
                function = 'turnOn'  # Function name for this action
            else:
                new_value = 'off'  # Power turned off
                function = 'turnOff'  # Function name for this action
        elif action == 'temperature':
            # Adjust the temperature (between 16°C and 30°C)
            new_value = random.randint(16, 30)
            function = 'setTemperature'  # Function name for this action
        elif action == 'fanSpeed':
            # Adjust the fan speed (low, medium, high)
            new_value = random.choice(['low', 'medium', 'high'])
            function = 'setFanSpeed'  # Function name for this action
        elif action == 'mode':
            # Change the mode (cooling, heating, fan-only)
            new_value = random.choice(['cooling', 'heating', 'fan-only'])
            function = 'setMode'  # Function name for this action

        # Update the state with the new value
        self.state[action] = new_value

        # Return the action details and the updated state
        return {
            'device_id': self.device_id,
            'user_id': self.user_id,
            'action': action,  # Action: 'power', 'temperature', 'fanSpeed', 'mode'
            'value': new_value,  # The new value of the action (e.g., 'on', 22, 'high', 'cooling')
            'function': function,  # Function name for the action (e.g., 'turnOn', 'setTemperature')
            'timestamp': current_time,  # The timestamp when the action was generated
            'state': self.state  # Current state of the device (for debugging or reference)
        }

