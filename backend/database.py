from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy instance for database interaction
db = SQLAlchemy()

# Define the SimulationLog model to represent logs in the database
class SimulationLog(db.Model):
    __tablename__ = 'transactions'  # Table name in the database
    
    id = db.Column(db.Integer, primary_key=True)
    device_type = db.Column(db.String(50), nullable=False)
    device_id = db.Column(db.String(130), nullable=False)
    user_id = db.Column(db.String(130), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(100), nullable=False)
    func = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    state = db.Column(db.String(500), nullable=False)

    def __init__(self, device_type, device_id, user_id, action, value, func, timestamp, state):
        self.device_type = device_type
        self.device_id = device_id
        self.user_id = user_id
        self.action = action
        self.value = value
        self.func = func
        self.timestamp = timestamp
        self.state = state

    def __repr__(self):
        return f"<SimulationLog {self.device_id} - {self.user_id} - {self.action} - {self.func}>"
