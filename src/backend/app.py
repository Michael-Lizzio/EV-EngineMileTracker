"""
Author Michael Lizzio
Date: 02/20/25
File: app.py
Workspace: EV-EngineMileTracker
"""

# Constants:
# None

# Imports:
from flask import Flask, session
from flask_session import Session
from datetime import timedelta
from src.backend.models import db
from src.backend.routes import app as routes_app
from src.backend.db_utils import build_db, rebuild_db  # Import database functions

app = Flask(__name__)

# Flask Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///engine_miles.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "supersecretkey"
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=1)

# Initialize Components
db.init_app(app)
Session(app)
app.register_blueprint(routes_app)

# Global Session Expiry Handling
@app.before_request
def refresh_session():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=1)

if __name__ == "__main__":
    app.run(debug=True)



