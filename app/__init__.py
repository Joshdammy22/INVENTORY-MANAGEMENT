from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from flask_mail import Mail



app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
bcrypt = Bcrypt(app)
socketio = SocketIO(app)
mail = Mail(app)

from . import routes, models, socketio_events

with app.app_context():
    db.create_all()