from flask import Flask, request, jsonify
from geopy.distance import geodesic
import time
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

previous_data = {
    'latitude': None,
    'longitude': None,
    'timestamp': None
}

@app.route('/update_location', methods=['POST'])
def update_location():
    global previous_data

    data = request.json
    latitude = data['latitude']
    longitude = data['longitude']
    timestamp = time.time()

    logging.debug(f'Received data: {data}')
    
    if previous_data['latitude'] is not None and previous_data['longitude'] is not None:
        prev_coords = (previous_data['latitude'], previous_data['longitude'])
        curr_coords = (latitude, longitude)
        
        distance = geodesic(prev_coords, curr_coords).meters 
        time_diff = timestamp - previous_data['timestamp']  

        if time_diff > 0:
            speed = distance / time_diff  
        else:
            speed = 0
    else:
        speed = 0

    previous_data['latitude'] = latitude
    previous_data['longitude'] = longitude
    previous_data['timestamp'] = timestamp

    logging.debug(f'Calculated speed: {speed} m/s')

    return jsonify({'speed': speed})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
