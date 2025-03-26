from flask import Flask, request, jsonify
from flask_cors import CORS
import openrouteservice

app = Flask(__name__)
CORS(app)  # Allow frontend to call the backend

# Replace with your OpenRouteService API Key
ORS_API_KEY = "5b3ce3597851110001cf6248b9aa70610e5d4dcaae9d9ef7ea9871d1"
client = openrouteservice.Client(key=ORS_API_KEY)

@app.route('/route', methods=['POST'])
def get_route():
    try:
        data = request.get_json()
        source = data['source']  # [longitude, latitude]
        destination = data['destination']  # [longitude, latitude]

        # Get the route from OpenRouteService
        route = client.directions(
            coordinates=[source, destination],
            profile='driving-car',
            format='geojson'
        )

        return jsonify(route)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
