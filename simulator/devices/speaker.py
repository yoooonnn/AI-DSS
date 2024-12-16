import random
from datetime import datetime

class Speaker:
    def __init__(self, device_id, user_id):
        self.device_type = "Speaker"
        self.device_id = device_id
        self.user_id = user_id
        self.state = {
            'power': 'off',  # Power status
            'volume': 50,    # Default volume (50%)
            'mode': 'normal',  # Mode (normal, party, etc.)
        }

    def generate_action(self, current_time):
        # Choose an action (power, music, voice assistant)
        action = random.choice(['power', 'voice assistant'])

        function = None
        new_value = None

        if action == 'power':
            # Toggle the power state
            if self.state['power'] == 'off':
                new_value = 'on'
                function = 'turnOn'
            else:
                new_value = 'off'
                function = 'turnOff'
            self.state['power'] = new_value
        elif action == 'voice assistant':
            new_value = random.choice(['weather', 'news', 'time', 'joke', 'reminder', 'music'])
            function = f'get{new_value.capitalize()}'

        return {
            'device_type': self.device_type,
            'device_id': self.device_id,
            'user_id': self.user_id,
            'action': action,
            'value': new_value,
            'function': function,
            'timestamp': current_time,
            'state': self.state
        }


# Simulate a Speaker object
speaker = Speaker(device_id="12345", user_id="user001")
current_time = datetime.now()

# Generate an action and check debug output
action_result = speaker.generate_action(current_time)

print(action_result)