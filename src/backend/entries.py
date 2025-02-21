from flask import Blueprint, request, jsonify
from src.backend.models import db, Entries

entries_bp = Blueprint("entries", __name__)

@entries_bp.route("/add_entry", methods=["POST"])
def add_entry():
    data = request.json
    required_fields = ["vehicle_id", "trip_odometer", "current_odometer", "gallons_added", "mpg", "date"]
    
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    previous_entry = Entries.query.filter_by(vehicle_id=data["vehicle_id"]).order_by(Entries.current_odometer.desc()).first()
    previous_odometer = previous_entry.current_odometer if previous_entry else 0

    if not data["current_odometer"]:
        data["current_odometer"] = previous_odometer + data["trip_odometer"]

    entry = Entries(**data)
    db.session.add(entry)
    db.session.commit()

    return jsonify({"message": "Entry added successfully!"}), 201
