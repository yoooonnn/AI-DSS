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
    }
}
