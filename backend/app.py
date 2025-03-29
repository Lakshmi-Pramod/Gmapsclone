from flask import Flask, request, jsonify
import requests
import sys
import time
from leader_election import Node

app = Flask(__name__)

# OpenRouteService API Key (Replace with your key)
ORS_API_KEY = "5b3ce3597851110001cf6248b9aa70610e5d4dcaae9d9ef7ea9871d1"

# Simulated distributed nodes
all_nodes = [1, 2, 3, 4, 5]

# Simulate node failures
failed_nodes = {5: True}  # Modify this to simulate different failures

# Get the node ID from the command line argument
if len(sys.argv) < 2:
    print("Usage: python app.py <node_id>")
    sys.exit(1)

try:
    current_node_id = int(sys.argv[1])  # Get node ID from CLI argument
except ValueError:
    print("Error: Node ID must be an integer.")
    sys.exit(1)

if current_node_id not in all_nodes:
    print(f"Error: Node {current_node_id} is not a valid node.")
    sys.exit(1)

# Function to check if a node is running
def check_node_status(node_id):
    """Check if a node is running by sending a request to its Flask server."""
    try:
        url = f"http://127.0.0.1:{5000 + node_id}/status"
        response = requests.get(url, timeout=1)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Dynamically detect active nodes
active_nodes = [n for n in all_nodes if check_node_status(n)]
if current_node_id not in active_nodes:
    active_nodes.append(current_node_id)

# Debugging logs
print(f"🧐 Debug: Current Node ID: {current_node_id}")
print(f"🧐 Debug: All Nodes: {all_nodes}")
print(f"🧐 Debug: Active Nodes Before Election: {active_nodes}")

# Start election process
node = Node(node_id=current_node_id, all_nodes=active_nodes)
node.start_election()

# Ensure the leader is set
elected_leader = node.leader if node.leader else max(active_nodes)

# Output startup details
print(f"🚀 Node {current_node_id} is running on Flask server...")
print(f"✅ Active Nodes: {active_nodes}")
print(f"❌ Failed Nodes: {[n for n in all_nodes if n not in active_nodes]}")
print(f"🏆 Current Leader: {elected_leader}")

@app.route("/status")
def status():
    """Returns 200 OK if this node is active."""
    return jsonify({"status": "active"}), 200

@app.route("/")
def home():
    """Home Route - Shows server is running and current node info."""
    return jsonify({
        "message": "Flask Server Running",
        "current_node": current_node_id,
        "active_nodes": active_nodes,
        "failed_nodes": [n for n in all_nodes if n not in active_nodes],
        "leader": elected_leader
    })

@app.route("/leader", methods=["GET"])
def get_leader():
    """Returns the current leader of the network."""
    return jsonify({"leader": elected_leader})

@app.route("/route", methods=["GET"])
def get_route():
    """Fetches a route using OpenRouteService API."""
    user_lat = request.args.get("user_lat")
    user_lng = request.args.get("user_lng")
    dest_lat = request.args.get("dest_lat")
    dest_lng = request.args.get("dest_lng")

    if not all([user_lat, user_lng, dest_lat, dest_lng]):
        return jsonify({"error": "Missing parameters"}), 400

    # OpenRouteService API URL
    route_url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={ORS_API_KEY}&start={user_lng},{user_lat}&end={dest_lng},{dest_lat}"

    response = requests.get(route_url)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch route", "status_code": response.status_code}), response.status_code

    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000 + current_node_id)  # Unique port per node
