"""
Author Michael Lizzio
Date: 02/20/25
File: routes.py
Workspace: EV-EngineMileTracker
"""

# Constants:
# None

# Imports:
from flask import Blueprint, request, render_template, jsonify
from src.backend.models import db, Users, Entries, Vehicle, Type
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt()


app = Blueprint('main', __name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add_entry", methods=["POST"])
def add_entire():
    data = request.json

    vehicle_id = data["vehicle_id"]
    trip_odometer = data["trip_odometer"]
    current_odometer = data["current_odometer"]
    gallons_added = data["gallons_added"]
    mpg = data["mpg"]
    date = data["date"]

    previous_entry = Entries.query.filter_by(vehicle_id=vehicle_id).order_by(Entries.current_odometer.desc()).first()

    previous_odometer = previous_entry.current_odometer if previous_entry else 0

    if current_odometer:
        trip_odometer = current_odometer - previous_odometer
    elif trip_odometer:
        current_odometer = previous_odometer + trip_odometer
    else:
        return jsonify({"message": "Missing trip_odometer or current_odometer"}), 400  # Bad request

    if gallons_added and mpg and date:
        entry = Entries(
            vehicle_id = data["vehicle_id"],
            trip_odometer = trip_odometer,
            current_odometer = current_odometer,
            gallons_added = data["gallons_added"],
            mpg = data["mpg"],
            date = data["date"]
        )

        db.session.add(entry)
        db.session.commit()

        return jsonify({"message": "Entry added successfully!"}), 201  # 201 Created

    else:
        return jsonify({"message": "Missing gallons_added or mpg or date"}), 400  # Bad request

@app.route("/add_vehicle", methods=["POST"])
def add_vehicle():
    data = request.json

    user_id = data["user_id"]
    name = data["name"]

    if not name:
        return jsonify({"message": "Missing name"}), 400  # Bad request

    existing_vehicle = Vehicle.query.filter_by(user_id=user_id).filter_by(name=name).first()
    if existing_vehicle:
        return jsonify({"message": "Vehicle already added"}), 409  # 409 Conflict

    entry = Vehicle(
        user_id = data["user_id"],
        name = data["name"]
    )

    db.session.add(entry)
    db.session.commit()

    return jsonify({"message": "Entry added successfully!"}), 201  # 201 Created


@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json

    # Validate input
    if "email" not in data or "password" not in data:
        return jsonify({"message": "Missing email or password"}), 400  # Bad request

    # Basic email validation
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, data["email"]):
        return jsonify({"message": "Invalid email format"}), 400

    # Check if email already exists
    existing_user = Users.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"message": "Email already in use"}), 409  # 409 Conflict

    # Hash password
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')

    user = Users(
        email=data["email"],
        hashed_password=hashed_password,
        active=True,
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User added successfully!"}), 201  # 201 Created

# Read
@app.route("/check_password", methods=["POST"])  # Use POST for security reasons
def check_password():
    data = request.json

    # Validate input
    if "email" not in data or "password" not in data:
        return jsonify({"message": "Missing email or password"}), 400

    user = Users.query.filter_by(email=data["email"]).first()

    if not user:    
        return jsonify({"message": "No user found"}), 404  # 404 Not Found
    
    if bcrypt.check_password_hash(user.hashed_password, data["password"]):
        return jsonify({"message": "Logged in successfully!"}), 200  # 200 OK
    
    else:
        return jsonify({"message": "Incorrect password"}), 401  # 401 Unauthorized


@app.route("/logout", methods=["POST"])
def logout():
    # session.clear()  # Remove all session data
    return jsonify({"message": "Logged out successfully!"}), 200


