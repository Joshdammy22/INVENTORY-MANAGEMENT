import os
from app import app
from dotenv import load_dotenv
from app import socketio

# Load environment variables from .env file
load_dotenv()


if __name__ == '__main__':
    socketio.run(app, debug=True)