from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory database for tracking users' locations
user_locations = {}

@app.route('/api/search', methods=['GET'])
def search_location():
    query = request.args.get('q')
    # Dummy response (Replace with Google Maps API / OpenStreetMap)
    return jsonify({"locations": [{"name": "New York", "lat": 40.7128, "lng": -74.0060}]})

@socketio.on('update_location')
def handle_update_location(data):
    user_id = data.get("user_id")
    lat, lng = data.get("lat"), data.get("lng")
    user_locations[user_id] = {"lat": lat, "lng": lng}
    emit("location_update", user_locations, broadcast=True)  # Broadcast to all clients

if __name__ == '__main__':
    socketio.run(app, debug=True)