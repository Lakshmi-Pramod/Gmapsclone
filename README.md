# Google Maps Clone

This project is a Google Maps clone built using Flask for the backend and React with Leaflet.js for the frontend. It features real-time location tracking and an interactive map interface.

## 🔥 Features
- **Flask Backend**: Handles API requests for location search and real-time location updates.
- **React Frontend**: Displays an interactive map using Leaflet.js.
- **WebSockets**: Utilizes Flask-SocketIO for real-time location updates.
- **PostgreSQL + PostGIS**: Optional support for spatial data storage.
- **Map Rendering**: Uses Google Maps API or OpenStreetMap via Leaflet.js.

## 📁 Project Structure
```
google-maps-clone
├── backend
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
├── frontend
│   ├── public
│   │   └── index.html
│   ├── src
│   │   ├── App.js
│   │   ├── index.js
│   │   └── styles.css
│   ├── package.json
│   └── README.md
└── README.md
```

## 🚀 Getting Started

### 1. Backend Setup
1. Navigate to the `backend` directory.
2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Start the Flask server:
   ```sh
   python app.py
   ```

### 2. Frontend Setup
1. Navigate to the `frontend` directory.
2. Install the required dependencies:
   ```sh
   npm install
   ```
3. Start the React application:
   ```sh
   npm start
   ```

## 🔄 Real-time Location Tracking
The application tracks user locations in real-time using WebSockets. When a user updates their location, it is broadcasted to all connected clients.

## 🔧 Future Enhancements
- Integrate Google Maps API for improved location accuracy.
- Store user locations in PostgreSQL/PostGIS for persistence.
- Implement route finding algorithms like Dijkstra’s or A*.
- Deploy the application using Docker and Nginx for better scalability.

## 📄 License
This project is open-source and available for modification and distribution.

git remote add origin https://github.com/Lakshmi-Pramod/Gmapsclone.git
git branch -M main
git push -u origin main