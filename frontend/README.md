# Frontend Documentation for Google Maps Clone

## Overview
This project is a Google Maps clone built using Flask for the backend and React with Leaflet.js for the frontend. It features real-time location tracking and an interactive map interface.

## Features
- Interactive map using Leaflet.js
- Real-time location updates via WebSockets
- User location tracking
- Search functionality for locations

## Getting Started

### Prerequisites
- Node.js and npm installed on your machine.
- Flask backend running on your local server.

### Installation
1. Navigate to the `frontend` directory:
   ```
   cd frontend
   ```

2. Install the required dependencies:
   ```
   npm install
   ```

### Running the Application
1. Start the Flask backend (make sure it's running on `http://127.0.0.1:5000`):
   ```
   cd backend
   python app.py
   ```

2. Start the React frontend:
   ```
   cd frontend
   npm start
   ```

3. Open your browser and go to `http://localhost:3000` to view the application.

## Usage
- Upon loading, the application will request permission to access your location.
- The map will display your current location and any other users' locations in real-time.
- You can search for locations using the provided API.

## Future Enhancements
- Integrate Google Maps API for enhanced features.
- Implement user authentication for personalized experiences.
- Store user locations in a database for persistence.
- Add routing capabilities to navigate between locations.

## Contributing
Feel free to submit issues or pull requests for any enhancements or bug fixes.