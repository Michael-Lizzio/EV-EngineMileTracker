from flask import Blueprint, request, jsonify
from src.backend.models import db, Entries

entries_bp = Blueprint("entries", __name__)

@entries_bp.route("/add_entry", methods=["POST"])
def add_entry():
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
