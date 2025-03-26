from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory list to store locations (instead of MongoDB)
locations = [
    {"name": "Location A", "lat": 10.123, "lng": 76.456},
    {"name": "Location B", "lat": 11.234, "lng": 77.567}
]

@app.route("/locations", methods=["GET"])
def get_locations():
    return jsonify(locations)

@app.route("/add_location", methods=["POST"])
def add_location():
    data = request.json
    locations.append(data)
    return jsonify({"message": "Location added"}), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)
