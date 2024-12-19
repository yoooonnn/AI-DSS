from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import sys
import logging
import os
import json
from datetime import datetime 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database import db, SimulationLog 

HTTP_200_OK = 200
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_422_UNPROCESSABLE_ENTITY = 422
HTTP_500_INTERNAL_SERVER_ERROR = 500

# Initialize the Flask application
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})


# Set up logging configuration
logging.basicConfig(
   level=logging.INFO,
   format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configure MySQL database URI
USERNAME = "root"
PASSWORD = ""
HOST = "localhost"  # MySQL 서버가 로컬에 있을 경우
DATABASE = "iotlogs"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"
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
        if not data:
            logging.error("No data provided in request")
            return jsonify({
                "status": "error",
                "code": HTTP_400_BAD_REQUEST,
                "message": "No data provided"
            }), HTTP_400_BAD_REQUEST
        
        if "logs" not in data:
            logging.error("No logs field in request data")
            return jsonify({
                "status": "error",
                "code": HTTP_422_UNPROCESSABLE_ENTITY,
                "message": "logs field is required"
            }), HTTP_422_UNPROCESSABLE_ENTITY
        
        logs = data["logs"]
        logging.info(f"Received {len(logs)} logs for processing")
        
        try:
            save_simulation_logs(logs)
            return jsonify({
                "status": "success",
                "code": HTTP_200_OK,
                "message": f"Successfully processed {len(logs)} logs"
            }), HTTP_200_OK
            
        except Exception as e:
            logging.error(f"Error in save_simulation_logs: {str(e)}")
            return jsonify({
                "status": "error",
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": f"Database error: {str(e)}"
            }), HTTP_500_INTERNAL_SERVER_ERROR
            
    except Exception as e:
        logging.error(f"Error processing the logs: {str(e)}")
        return jsonify({
            "status": "error",
            "code": HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR

@app.route('/get_logs', methods=['GET'])
def get_logs():
    try:
        logs = SimulationLog.query.order_by(SimulationLog.timestamp.desc()).all()
        
        if not logs:
            return jsonify({
                "status": "success",
                "code": HTTP_200_OK,
                "data": [],
                "message": "No logs found"
            }), HTTP_200_OK
            
        logs_data = []
        for log in logs:
            try:
                state = json.loads(log.state)
            except:
                state = log.state

            logs_data.append({
                'id': log.id,
                'device_type': log.device_type,
                'device_id': log.device_id,
                'user_id': log.user_id,
                'action': log.action,
                'value': log.value,
                'func': log.func,
                'timestamp': log.timestamp.isoformat(),
                'state': state
            })

        return jsonify({
            "status": "success",
            "code": HTTP_200_OK,
            "data": logs_data
        }), HTTP_200_OK
        
    except Exception as e:
        logging.error(f"Error fetching logs: {str(e)}")
        return jsonify({
            "status": "error",
            "code": HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR

@app.route('/get_logs', methods=['OPTIONS'])
def handle_options():
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Accept')
    return response


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
               device_type=log['device_type'],
               device_id=log['device_id'],
               user_id=log['user_id'],
               action=log['action'],
               value=str(log['value']),
               func=log['func'],
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

if __name__ == '__main__':
   app.run(debug=True)
