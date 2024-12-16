import random

# Possible states and actions for the light device
light_states = {
    'power': ['on', 'off'],
    'brightness': range(0, 101),  # 0-100%
    'color_temp': range(2700, 6501)  # 2700K-6500K
}

# Light device class
class Light:
    def __init__(self, device_id, user_id):
        self.device_id = device_id
        self.user_id = user_id
        self.state = {
            'power': 'off',  # Initial power state is 'off'
            'brightness': 0,  # Initial brightness is 0
            'color_temp': 2700  # Initial color temperature is 2700K
        }
        
    def generate_action(self, current_time):
        # Apply weights for actions based on time of day (e.g., used more frequently in the evening)
        hour = current_time.hour
        if 6 <= hour < 9:  # Morning
            action_weights = {'power': 0.6, 'brightness': 0.3, 'color_temp': 0.1}
        elif 17 <= hour < 23:  # Evening
            action_weights = {'power': 0.4, 'brightness': 0.4, 'color_temp': 0.2}
        else:  # Other times of the day
            action_weights = {'power': 0.8, 'brightness': 0.1, 'color_temp': 0.1}
            
        # Choose an action based on the weighted probabilities
        action = random.choices(list(action_weights.keys()), 
                                list(action_weights.values()))[0]
                              
        # Generate new state based on selected action
        if action == 'power':
            new_value = 'on' if self.state['power'] == 'off' else 'off'
        elif action == 'brightness':
            new_value = random.randint(0, 100)  # Random brightness between 0 and 100
        else:  # color_temp
            new_value = random.randint(2700, 6500)  # Random color temperature between 2700K and 6500K
            
        # Return the action details as a dictionary
        return {
            'device_id': self.device_id,
            'user_id': self.user_id,
            'action': action,
            'value': new_value,
            'timestamp': current_time  # Time when the action was generated
        }
