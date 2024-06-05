import os
from dotenv import load_dotenv
from app import app, socketio

# Load environment variables from .env file
load_dotenv()


if __name__ == '__main__':
    socketio.run(app, debug=True)


