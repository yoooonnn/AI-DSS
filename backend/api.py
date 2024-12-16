from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, SimulationLog
from datetime import datetime
import os
import sys

# Initialize the Flask application
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Get the current directory and ensure the 'data' folder exists
db_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')  # 'data' folder path
os.makedirs(db_dir, exist_ok=True)  # Ensure 'data' folder exists

# Configure SQLite database URI for storing logs
db_path = os.path.join(db_dir, 'simulation_logs.db')  # SQLite database path
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'  # Set the URI for SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance

# Initialize SQLAlchemy with Flask app
db.init_app(app)

# Add the current directory to the Python path to ensure 'simulator' can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'simulator'))

# Function to save simulation logs to the database
def save_simulation_logs(logs):
    """Save the list of simulation logs to the database."""
    for log in logs:
        simulation_log = SimulationLog(
            device_id=log['device_id'],
            user_id=log['user_id'],
            action=log['action'],
            value=log['value'],
            timestamp=log['timestamp']
        )
        db.session.add(simulation_log)  # Add log to the session
    db.session.commit()  # Commit changes to the database

# API endpoint for running the simulation
@app.route('/simulate', methods=['POST'])
def simulate():
    """
    API endpoint to simulate the smart home environment, 
    running for a specified duration and start time.
    """
    # Get simulation parameters (duration and start time) from the request
    duration_hours = request.json.get('duration_hours', 24)  # Default to 24 hours
    start_time_str = request.json.get('start_time', '2024-12-16 00:00:00')  # Default start time
    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')  # Convert to datetime

    # Run the simulator (imported from the simulator module)
    from simulator import SmartHomeSimulator  # Import after modifying sys.path
    simulator = SmartHomeSimulator()
    simulator.simulate(start_time, duration_hours)  # Run simulation

    # Save the simulation logs to the database
    save_simulation_logs(simulator.logs)

    # Return a response containing the simulation status and logs
    return jsonify({"status": "success", "logs": [log for log in simulator.logs]}), 200

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=False)  # Start the Flask app in debug mode
