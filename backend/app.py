from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# OpenRouteService API Key (Replace with your key)
ORS_API_KEY = "5b3ce3597851110001cf6248b9aa70610e5d4dcaae9d9ef7ea9871d1"

@app.route("/route", methods=["GET"])
def get_route():
    user_lat = request.args.get("user_lat")
    user_lng = request.args.get("user_lng")
    dest_lat = request.args.get("dest_lat")
    dest_lng = request.args.get("dest_lng")

    if not all([user_lat, user_lng, dest_lat, dest_lng]):
        return jsonify({"error": "Missing parameters"}), 400

    # OpenRouteService API URL
    route_url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={ORS_API_KEY}&start={user_lng},{user_lat}&end={dest_lng},{dest_lat}"

    response = requests.get(route_url)
    data = response.json()

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
