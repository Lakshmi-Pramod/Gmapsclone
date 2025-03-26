import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import io from "socket.io-client";
import "leaflet/dist/leaflet.css";

const socket = io("http://127.0.0.1:5000"); // Connect to Flask WebSockets

const App = () => {
  const [userLocation, setUserLocation] = useState(null);
  const [otherUsers, setOtherUsers] = useState({});

  // Get user location on load
  useEffect(() => {
    navigator.geolocation.getCurrentPosition((position) => {
      const { latitude, longitude } = position.coords;
      setUserLocation({ lat: latitude, lng: longitude });

      // Send location to server
      socket.emit("update_location", { user_id: "user123", lat: latitude, lng: longitude });
    });

    // Listen for location updates
    socket.on("location_update", (locations) => {
      setOtherUsers(locations);
    });

    return () => socket.disconnect();
  }, []);

  return (
    <div>
      <h2>Google Maps Clone (Leaflet.js + Flask)</h2>
      <MapContainer center={[51.505, -0.09]} zoom={13} style={{ height: "80vh", width: "100%" }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        
        {userLocation && (
          <Marker position={[userLocation.lat, userLocation.lng]}>
            <Popup>You are here!</Popup>
          </Marker>
        )}

        {Object.entries(otherUsers).map(([userId, location]) => (
          <Marker key={userId} position={[location.lat, location.lng]}>
            <Popup>User {userId}</Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default App;