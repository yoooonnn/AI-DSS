import random

# Possible states and actions for the light device
light_states = {
    'power': ['on', 'off'],
    'brightness': range(0, 101),  # 0-100%
    'color': ['red', 'green', 'blue', 'yellow', 'white'],  # Example color states
    'mode': ['normal', 'night', 'reading', 'party']  # Different modes
}

# Light device class
class Light:
    def __init__(self, device_id, user_id):
        self.device_type = 'Light'
        self.device_id = device_id
        self.user_id = user_id
        self.state = {
            'power': 'off',  # Initial power state is 'off'
            'brightness': 0,  # Initial brightness is 0
            'color': 'white',  # Default color is white
            'mode': 'normal'  # Default mode is normal
        }

    def generate_action(self, current_time):
        # Apply weights for actions based on time of day (e.g., used more frequently in the evening)
        hour = current_time.hour
        if 6 <= hour < 9:  # Morning
            action_weights = {'power': 0.5, 'brightness': 0.3, 'setMode': 0.1, 'setColor': 0.1}
        elif 17 <= hour < 23:  # Evening
            action_weights = {'power': 0.4, 'brightness': 0.3, 'setMode': 0.2, 'setColor': 0.1}
        else:  # Other times of the day
            action_weights = {'power': 0.6, 'brightness': 0.2, 'setMode': 0.1, 'setColor': 0.1}

        # Choose an action based on the weighted probabilities
        action = random.choices(list(action_weights.keys()), 
                                list(action_weights.values()))[0]

        # Initialize the function variable
        function = None
        new_value = None

        # Generate new state based on selected action
        if action == 'power':
            # When turning on or off, set the appropriate action name
            if self.state['power'] == 'off':
                new_value = 'on'  # Power turned on
                self.state['power'] = 'on'
                function = 'turnOn'  # Function name for this action
            else:
                new_value = 'off'  # Power turned off
                self.state['power'] = 'off'
                function = 'turnOff'  # Function name for this action
        elif action == 'brightness':
            new_value = random.randint(0, 100)  # Random brightness between 0 and 100
            self.state['brightness'] = new_value
            function = 'setBrightness'  # Function name for brightness adjustment
        elif action == 'setMode':
            new_value = random.choice(light_states['mode'])  # Random mode (e.g., night, reading, etc.)
            self.state['mode'] = new_value
            function = 'setMode'  # Function name for mode adjustment
        elif action == 'setColor':
            new_value = random.choice(light_states['color'])  # Random color
            self.state['color'] = new_value
            function = 'setColor'  # Function name for color adjustment

        # Ensure that 'function' is always set before returning the dictionary
        return {
            'device_type': self.device_type,
            'device_id': self.device_id,
            'user_id': self.user_id,
            'action': action,  # 'mode', 'color', 'brightness', 'power' etc.
            'value': new_value,
            'function': function,  # 'turnOn', 'setBrightness', 'setColor', 'setMode', etc.
            'timestamp': current_time,  # Time when the action was generated
            'state': self.state  # Current state after action
        }