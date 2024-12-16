from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, SimulationLog 
import logging
import os
import json
from datetime import datetime 

# Initialize the Flask application
app = Flask(__name__)

# Set up logging configuration
logging.basicConfig(
   level=logging.INFO,
   format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configure database path and create directory if needed
db_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
os.makedirs(db_dir, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(db_dir, "simulation_logs.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with Flask app
db.init_app(app)

# Drop existing tables and create new ones
with app.app_context():
   db.drop_all()
   db.create_all()
   logging.info("Database tables created successfully")

@app.route('/simulate', methods=['POST'])
def simulate():
   try:
       data = request.json

       if not data or "logs" not in data:
           logging.error("No logs data provided in request")
           return jsonify({"status": "error", "message": "No logs data provided"}), 400
       
       logs = data["logs"]
       logging.info(f"Received {len(logs)} logs for processing")
       try:
           save_simulation_logs(logs)
           return jsonify({"status": "success", "message": f"Successfully processed {len(logs)} logs"}), 200
       except Exception as e:
           logging.error(f"Error in save_simulation_logs: {str(e)}")
           return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500
   except Exception as e:
       logging.error(f"Error processing the logs: {str(e)}")
       return jsonify({"status": "error", "message": str(e)}), 500

def save_simulation_logs(logs):
   try:
       for log in logs:
           # Convert state to string if it's a dictionary
           state = json.dumps(log['state']) if isinstance(log['state'], dict) else str(log['state'])
           
           # Handle ISO format timestamp 
           if isinstance(log['timestamp'], str):
               try:
                   timestamp = datetime.fromisoformat(log['timestamp'].replace('T', ' '))
               except Exception as e:
                   logging.error(f"Error parsing timestamp: {log['timestamp']}")
                   timestamp = datetime.now()  # Use current time if parsing fails
           else:
               timestamp = log['timestamp']

           simulation_log = SimulationLog(
               device_id=log['device_id'],
               user_id=log['user_id'],
               action=log['action'],
               value=str(log['value']),
               function=log['function'],
               timestamp=timestamp,
               state=state
           )
           db.session.add(simulation_log)
           
       db.session.commit()
       logging.info(f"Successfully saved {len(logs)} logs to database")
   except Exception as e:
       logging.error(f"Error saving logs to database: {e}")
       db.session.rollback()
       raise

# Run the Flask application in debug mode
if __name__ == '__main__':
   app.run(debug=True)