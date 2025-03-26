# Backend Documentation for Google Maps Clone

## Overview
This backend is built using Flask and provides an API for location searches and real-time location tracking using WebSockets. It serves as the server-side component of the Google Maps clone application.

## Features
- **Location Search API**: Allows users to search for locations.
- **Real-time Location Updates**: Utilizes Flask-SocketIO to broadcast user location updates to all connected clients.
- **In-memory User Tracking**: Maintains a dictionary to track user locations during the session.

## Setup Instructions

### Prerequisites
- Python 3.x
- pip (Python package installer)

### Installation
1. Navigate to the `backend` directory:
   ```
   cd backend
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the Application
1. Start the Flask server:
   ```
   python app.py
   ```

2. The server will run on `http://127.0.0.1:5000`.

## Usage
- The API endpoint for searching locations is available at `/api/search?q={query}`.
- To receive real-time location updates, connect to the WebSocket server at `http://127.0.0.1:5000`.

## Future Enhancements
- Integrate with Google Maps API for enhanced location data.
- Implement persistent storage using PostgreSQL/PostGIS.
- Add route finding capabilities.

## License
This project is licensed under the MIT License.