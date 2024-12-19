# simulator/log_api_handler.py

from datetime import datetime, timedelta
import requests
import logging
import json

# Set backend API URL
API_URL = "http://127.0.0.1:5000/simulate"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder for handling datetime objects"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO format string
        return super().default(obj)

def process_log_data(log_data):
    """
    Process log data to convert all datetime objects into serializable format
    :param log_data: Log data to process
    :return: Log data with serialized datetime values
    """
    processed_logs = []
    
    for log in log_data:
        processed_log = {}
        for key, value in log.items():
            if isinstance(value, datetime):
                processed_log[key] = value.isoformat()
            elif isinstance(value, dict):
                # Handle nested dictionaries (like 'state')
                processed_log[key] = {
                    k: v.isoformat() if isinstance(v, datetime) else v
                    for k, v in value.items()
                }
            else:
                processed_log[key] = value
        processed_logs.append(processed_log)
    
    return processed_logs

def send_log_to_backend(log_data):
    """
    Send log data to the backend
    :param log_data: Log data to be sent
    :return: Backend response or None if failed
    """
    try:
        # Process datetime objects
        processed_logs = process_log_data(log_data)
        
        # Print log data being sent
        logging.info(f"Sending log data to backend: {json.dumps(processed_logs, indent=2, ensure_ascii=False)}")
        
        # Send logs via POST request
        response = requests.post(API_URL, json={"logs": processed_logs})
        
        if response.status_code == 200:
            logging.info("Logs successfully sent.")
            return response.json()
        else:
            logging.error(f"Failed to send logs: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Backend communication error: {e}")
        return None

def handle_log(logs):
    """
    Process and send log data to backend
    :param logs: List of logs to send
    :return: None
    """
    logging.info(f"Starting to send logs: {len(logs)} logs total")
    
    result = send_log_to_backend(logs)
    
    if result:
        logging.info(f"Response data: {result}")
    else:
        logging.error("Failed to send logs")