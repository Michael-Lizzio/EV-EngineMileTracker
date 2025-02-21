"""
Author Michael Lizzio
Date: 02/20/25
File: models.py
Workspace: EV-EngineMileTracker
"""

# Constants:
# None

# Imports:
# None

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Entries(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    vehicle_id = db.Column(db.Integer, nullable=False)
    trip_odometer = db.Column(db.Float, nullable=False)
    current_odometer = db.Column(db.Float, nullable=False)
    gallons_added = db.Column(db.Float, nullable=False)
    mpg = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(20), nullable=False, unique=True)

# class Type(db.Model):
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     vehicle_type = db.Column(db.String(20), nullable=False)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    hashed_password = db.Column(db.String(61), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)





