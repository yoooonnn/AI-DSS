user_patterns = {
    'Office Worker': {
        'active_hours': [(6, 9), (18, 23)],
        'interaction_probability': {
            'weekday': 0.7,
            'weekend': 0.9
        }
    },
    'Remote Worker': {
        'active_hours': [(8, 22)],
        'interaction_probability': {
            'weekday': 0.8,
            'weekend': 0.9
        }
    },
    'Student': {
        'active_hours': [(7, 9), (14, 24)],
        'interaction_probability': {
            'weekday': 0.6,
            'weekend': 0.95
        }
    },
    'Stay-at-home Parent': {
        'active_hours': [(6, 22)],
        'interaction_probability': {
            'weekday': 0.85,
            'weekend': 0.9
        }
    },
    'Night Shift Worker': {
        'active_hours': [(5, 8), (16, 19)],  # Sleep during day, active evening/early morning
        'interaction_probability': {
            'weekday': 0.7,
            'weekend': 0.8
        }
    },
    'Elderly Resident': {
        'active_hours': [(5, 21)],  # Early riser, earlier bedtime
        'interaction_probability': {
            'weekday': 0.75,
            'weekend': 0.75  # Consistent throughout week
        }
    },
    'Freelancer': {
        'active_hours': [(9, 23)],  # Flexible schedule
        'interaction_probability': {
            'weekday': 0.75,
            'weekend': 0.85
        }
    },
    'Weekend Traveler': {
        'active_hours': [(6, 9), (17, 23)],  # Similar to office worker on weekdays
        'interaction_probability': {
            'weekday': 0.7,
            'weekend': 0.3  # Lower probability due to travel
        }
    },
    'Family with Kids': {
        'active_hours': [(6, 8), (15, 22)],  # Morning rush and evening family time
        'interaction_probability': {
            'weekday': 0.85,
            'weekend': 0.95
        }
    },
    'Fitness Enthusiast': {
        'active_hours': [(5, 7), (17, 22)],  # Early morning workout, evening routine
        'interaction_probability': {
            'weekday': 0.8,
            'weekend': 0.9
        }
    }
}