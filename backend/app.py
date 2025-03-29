from flask import Flask, request, jsonify
import requests
import sys
import time
import threading
from leader_election import Node

app = Flask(__name__)

# OpenRouteService API Key (Replace with your key)
ORS_API_KEY = "5b3ce3597851110001cf6248b9aa70610e5d4dcaae9d9ef7ea9871d1"

# Simulated distributed nodes
all_nodes = [1, 2, 3, 4, 5]
failed_nodes = {5: True}  # Simulating failure

# Get the node ID from the command line argument
if len(sys.argv) < 2:
    print("Usage: python app.py <node_id>")
    sys.exit(1)

try:
    current_node_id = int(sys.argv[1])
except ValueError:
    print("Error: Node ID must be an integer.")
    sys.exit(1)

if current_node_id not in all_nodes:
    print(f"Error: Node {current_node_id} is not a valid node.")
    sys.exit(1)

# Check if nodes are running
def check_node_status(node_id):
    """Check if a node is running by sending a request to its Flask server."""
    try:
        url = f"http://127.0.0.1:{5000 + node_id}/status"
        response = requests.get(url, timeout=1)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Detect active nodes dynamically
active_nodes = [n for n in all_nodes if check_node_status(n)]
if current_node_id not in active_nodes:
    active_nodes.append(current_node_id)

# Leader election
node = Node(node_id=current_node_id, all_nodes=active_nodes)
node.start_election()
elected_leader = node.leader if node.leader else max(active_nodes)

# Snapshot storage
snapshots = {}
received_markers = set()
channel_states = {}

# Initiate snapshot
def initiate_snapshot():
    global snapshots, received_markers, channel_states
    print(f"📸 Node {current_node_id} initiating snapshot...")

    snapshots[current_node_id] = {
        "state": {"leader": elected_leader, "active_nodes": active_nodes},
        "messages": {},
    }
    received_markers.add(current_node_id)

    # Send marker messages to all active nodes
    for node_id in active_nodes:
        if node_id != current_node_id:
            send_marker(node_id)

# Send marker to another node
def send_marker(node_id):
    """Send a marker message to another node."""
    try:
        url = f"http://127.0.0.1:{5000 + node_id}/receive_marker"
        requests.post(url, json={"from": current_node_id})
        print(f"📩 Marker sent from {current_node_id} to {node_id}")
    except requests.exceptions.RequestException:
        print(f"❌ Failed to send marker to Node {node_id}")

@app.route("/receive_marker", methods=["POST"])
def receive_marker():
    """Handle marker receipt."""
    global snapshots, received_markers, channel_states

    sender = request.json.get("from")
    print(f"📥 Marker received at Node {current_node_id} from Node {sender}")

    if current_node_id not in received_markers:
        # Record state and start snapshot
        snapshots[current_node_id] = {
            "state": {"leader": elected_leader, "active_nodes": active_nodes},
            "messages": {},
        }
        received_markers.add(current_node_id)

        # Send markers to all nodes
        for node_id in active_nodes:
            if node_id != current_node_id:
                send_marker(node_id)

    return jsonify({"message": "Marker received"}), 200

@app.route("/get_snapshot", methods=["GET"])
def get_snapshot():
    """Retrieve the latest snapshot."""
    return jsonify(snapshots)

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

    def fetch_route():
        thread_name = threading.current_thread().name
        print(f"🚦 [THREAD {thread_name}] Processing route request...")

        route_url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={ORS_API_KEY}&start={user_lng},{user_lat}&end={dest_lng},{dest_lat}"
        response = requests.get(route_url)

        if response.status_code != 200:
            print(f"❌ [THREAD {thread_name}] Failed to fetch route: {response.status_code}")
            return jsonify({"error": "Failed to fetch route", "status_code": response.status_code}), response.status_code
        
        print(f"✅ [THREAD {thread_name}] Successfully fetched route.")
        return jsonify(response.json())

    route_thread = threading.Thread(target=fetch_route, name=f"Node-{current_node_id}-Thread")
    route_thread.start()

    return jsonify({"message": "Route request processing started"})

if __name__ == "__main__":
    if current_node_id == elected_leader:
        threading.Timer(5, initiate_snapshot).start()  # Start snapshot if leader

    app.run(debug=True, host="0.0.0.0", port=5000 + current_node_id)
