"""
Author Michael Lizzio
Date: 02/20/25
File: routes.py
Workspace: EV-EngineMileTracker
"""

# Constants:
# None

# Imports:
from flask import Blueprint
from src.backend.auth import auth_bp
from src.backend.vehicle import vehicle_bp
from src.backend.entries import entries_bp

app = Blueprint('main', __name__)

@app.route("/")
def home():
    return render_template("index.html")

# Register the submodules
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(vehicle_bp, url_prefix="/vehicle")
app.register_blueprint(entries_bp, url_prefix="/entries")



