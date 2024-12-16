import requests
import json

url = 'http://127.0.0.1:5000/simulate'
headers = {'Content-Type': 'application/json'}

data = {
    'duration_hours': 24,
    'start_time': '2024-12-16 00:00:00'
}

response = requests.post(url, headers=headers, data=json.dumps(data))

# Print the response from the server
print(response.status_code)  # Should return 200 if successful
print(response.json())  # The response body containing the logs and status
