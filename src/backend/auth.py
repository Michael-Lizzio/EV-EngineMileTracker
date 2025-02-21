from flask import Blueprint, request, jsonify, session
from src.backend.models import db, Users
from flask_bcrypt import Bcrypt
from datetime import timedelta
import re

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()

# Register User
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    if "email" not in data or "password" not in data:
        return jsonify({"message": "Missing email or password"}), 400

    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, data["email"]):
        return jsonify({"message": "Invalid email format"}), 400

    existing_user = Users.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"message": "Email already in use"}), 409

    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    user = Users(email=data["email"], hashed_password=hashed_password, active=True)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

# Login User
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = Users.query.filter_by(email=data["email"]).first()

    if not user or not bcrypt.check_password_hash(user.hashed_password, data["password"]):
        return jsonify({"message": "Invalid email or password"}), 401

    session["user_id"] = user.id
    session["email"] = user.email
    session.permanent = True

    return jsonify({"message": "Logged in successfully!", "user_id": user.id}), 200

# Check if user session is still valid
@auth_bp.route("/auth/check_session", methods=["GET"])
def check_session():
    if "user_id" in session:
        return jsonify({"message": "User is logged in", "email": session["email"]}), 200
    return jsonify({"message": "User not logged in"}), 401  # If session expired, log them out

@auth_bp.route("/auth/logout", methods=["POST"])
def logout():
    session.clear()  # Remove all session data
    return jsonify({"message": "Logged out successfully!"}), 200
