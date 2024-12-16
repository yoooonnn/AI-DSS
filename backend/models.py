from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy instance for database interaction
db = SQLAlchemy()

# Define the SimulationLog model to represent logs in the database
class SimulationLog(db.Model):
    __tablename__ = 'simulation_logs'  # Table name in the database
    
    # Define columns in the simulation_logs table
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each log
    device_id = db.Column(db.String(50), nullable=False)  # ID of the device
    user_id = db.Column(db.String(50), nullable=False)  # ID of the user
    action = db.Column(db.String(50), nullable=False)  # Action performed on the device
    value = db.Column(db.String(100), nullable=False)  # Value associated with the action
    function = db.Column(db.String(50), nullable=False)  # Function name triggered
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Timestamp of the action
    state = db.Column(db.String(500), nullable=False) 

    
    def __init__(self, device_id, user_id, action, value, function, timestamp, state):
        self.device_id = device_id
        self.user_id = user_id
        self.action = action
        self.value = value
        self.function = function
        self.timestamp = timestamp
        self.state = state

    def __repr__(self):
        return f"<SimulationLog {self.device_id} - {self.user_id} - {self.action} - {self.function}>"
