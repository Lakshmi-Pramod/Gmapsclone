import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Polyline } from "react-leaflet";
import axios from "axios";
import "leaflet/dist/leaflet.css";

const App = () => {
    const [source, setSource] = useState([10.9027, 76.9006]); // Default: Ettimadai
    const [destination, setDestination] = useState("");
    const [route, setRoute] = useState([]);
    const [error, setError] = useState("");

    // Function to get coordinates of a place
    const getCoordinates = async (place) => {
        try {
            const response = await axios.get(
                `https://nominatim.openstreetmap.org/search?format=json&q=${place}`
            );
            if (response.data.length > 0) {
                return [parseFloat(response.data[0].lon), parseFloat(response.data[0].lat)];
            } else {
                throw new Error("Location not found");
            }
        } catch (error) {
            console.error("Error fetching coordinates:", error);
            setError("Location not found.");
            return null;
        }
    };

    // Function to fetch the route
    const handleSearch = async () => {
        setError(""); // Clear previous errors
        if (!destination) return;

        const destinationCoords = await getCoordinates(destination);
        if (!destinationCoords) return;

        try {
            const response = await axios.post("http://127.0.0.1:5000/route", {
                source,
                destination: destinationCoords,
            });

            if (response.data.routes) {
                setRoute(response.data.routes[0].geometry.coordinates.map(([lon, lat]) => [lat, lon]));
            } else {
                setError("No route found.");
            }
        } catch (error) {
            console.error("Error fetching route:", error);
            setError("Failed to fetch route.");
        }
    };

    return (
        <div style={{ textAlign: "center", padding: "20px" }}>
            <h2>Smart City Navigation (Using OpenRouteService)</h2>
            <input
                type="text"
                placeholder="Enter destination..."
                value={destination}
                onChange={(e) => setDestination(e.target.value)}
                style={{ padding: "8px", marginRight: "8px" }}
            />
            <button onClick={handleSearch} style={{ padding: "8px", cursor: "pointer" }}>
                Search Route
            </button>

            {error && <p style={{ color: "red" }}>{error}</p>}

            <MapContainer center={source} zoom={14} style={{ height: "500px", width: "100%", marginTop: "20px" }}>
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                <Marker position={source} />
                {route.length > 0 && <Polyline positions={route} color="red" />}
            </MapContainer>
        </div>
    );
};

export default App;
