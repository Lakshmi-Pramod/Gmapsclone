import React, { useEffect, useState, useRef } from "react";
import { MapContainer, TileLayer, Marker, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import "leaflet-routing-machine";
import "./styles.css"; // Import the CSS file

const DEFAULT_CENTER = [10.9027, 76.9006]; // Ettimadai, Coimbatore

// 🟢 Custom Icon for User & Destination Markers
const customIcon = new L.Icon({
  iconUrl: require("./marker.png"), // Replace with your marker image
  iconSize: [40, 40], // Adjust size if needed
  iconAnchor: [20, 40],
  popupAnchor: [0, -40],
});

const Routing = ({ userLocation, destination, setDirections }) => {
  const map = useMap();
  const routingControlRef = useRef(null);

  useEffect(() => {
    if (!userLocation || !destination || !map) return;

    if (routingControlRef.current) {
      map.removeControl(routingControlRef.current);
      routingControlRef.current = null;
      setDirections([]);
    }

    const routingControl = L.Routing.control({
      waypoints: [
        L.latLng(userLocation[0], userLocation[1]),
        L.latLng(destination[0], destination[1]),
      ],
      routeWhileDragging: true,
      createMarker: () => null,
      show: false,
      addWaypoints: false,
      draggableWaypoints: false,
      fitSelectedRoutes: true,
      router: L.Routing.osrmv1({ profile: "driving" }),
    }).addTo(map);

    routingControlRef.current = routingControl;

    routingControl.on("routesfound", function (e) {
      const routes = e.routes[0].instructions.map((step) => step.text);
      setDirections(routes);
    });

    return () => {
      if (routingControlRef.current) {
        map.removeControl(routingControlRef.current);
        routingControlRef.current = null;
      }
    };
  }, [userLocation, destination, map, setDirections]);

  return null;
};

const App = () => {
  const [userLocation, setUserLocation] = useState(null);
  const [destination, setDestination] = useState(null);
  const [searchInput, setSearchInput] = useState("");
  const [directions, setDirections] = useState([]);
  const [showPopup, setShowPopup] = useState(false); // Controls visibility of the popup

  useEffect(() => {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setUserLocation([position.coords.latitude, position.coords.longitude]);
      },
      () => {
        alert("Could not get your location.");
      }
    );
  }, []);

  const handleSearch = async () => {
    if (!searchInput) return alert("Please enter a destination");

    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${searchInput}`
      );
      const data = await response.json();

      if (data.length > 0) {
        setDestination([data[0].lat, data[0].lon]);
        setShowPopup(true); // Show the popup when search is performed
      } else {
        alert("Location not found. Try a different place.");
      }
    } catch (error) {
      alert("Error fetching location.");
    }
  };

  return (
    <div className="app-container">
      {/* 🔍 Search Bar */}
      <div className="search-container">
        <input
          type="text"
          placeholder="Enter destination"
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
        />
        <button onClick={handleSearch}>Search Route</button>
      </div>

      {/* 🗺️ Fullscreen Map */}
      <div className="map-container">
        <MapContainer center={DEFAULT_CENTER} zoom={12} className="fullscreen-map">
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          {userLocation && <Marker position={userLocation} icon={customIcon} />}
          {destination && <Marker position={destination} icon={customIcon} />}
          {userLocation && destination && (
            <Routing
              key={destination ? `${destination[0]}-${destination[1]}` : "initial"}
              userLocation={userLocation}
              destination={destination}
              setDirections={setDirections}
            />
          )}
        </MapContainer>
      </div>

      {/* 📜 Directions Popup */}
      {showPopup && (
        <div className="directions-popup">
          <button className="close-btn" onClick={() => setShowPopup(false)}>❌</button>
          <h2>Directions</h2>
          {directions.length === 0 && destination && <p>Fetching directions...</p>}
          {directions.length > 0 && (
            <ol>
              {directions.map((step, index) => (
                <li key={index}>{step}</li>
              ))}
            </ol>
          )}
        </div>
      )}
    </div>
  );
};

export default App;
