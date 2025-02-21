from flask import Blueprint, request, jsonify
from src.backend.models import db, Vehicle

vehicle_bp = Blueprint("vehicle", __name__)

@vehicle_bp.route("/add_vehicle", methods=["POST"])
def add_vehicle():
    data = request.json
    if "user_id" not in data or "name" not in data:
        return jsonify({"message": "Missing user_id or name"}), 400

    existing_vehicle = Vehicle.query.filter_by(user_id=data["user_id"], name=data["name"]).first()
    if existing_vehicle:
        return jsonify({"message": "Vehicle already exists"}), 409

    vehicle = Vehicle(user_id=data["user_id"], name=data["name"])
    db.session.add(vehicle)
    db.session.commit()

    return jsonify({"message": "Vehicle added successfully!"}), 201
