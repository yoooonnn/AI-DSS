from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance for database interaction
db = SQLAlchemy()

# Define the SimulationLog model to represent logs in the database
class SimulationLog(db.Model):
    __tablename__ = 'simulation_logs'  # Table name in the database
    
    # Define columns in the simulation_logs table
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each log
    device_id = db.Column(db.Integer, nullable=False)  # ID of the device that generated the log
    user_id = db.Column(db.Integer, nullable=False)  # ID of the user who interacted with the device
    action = db.Column(db.String(50), nullable=False)  # Action performed on the device (e.g., 'power', 'brightness')
    value = db.Column(db.String(100), nullable=False)  # Value associated with the action (e.g., 'on', 75, '3000K')
    timestamp = db.Column(db.DateTime, nullable=False)  # Timestamp when the action occurred

    def __init__(self, device_id, user_id, action, value, timestamp):
        # Initialize a new SimulationLog instance with provided parameters
        self.device_id = device_id
        self.user_id = user_id
        self.action = action
        self.value = value
        self.timestamp = timestamp

    def __repr__(self):
        # Return a string representation for easy debugging
        return f"<SimulationLog {self.device_id} - {self.user_id}>"
