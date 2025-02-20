from flask import Blueprint, request, render_template, jsonify
from src.models import db, Trip

app = Blueprint('app', __name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_trip", methods=["POST"])
def add_trip():
    data = request.json
    trip = Trip(
        date=data['date'],
        odometer_start=data['odometer_start'],
        odometer_end=data['odometer_end'],
        gallons_used=data['gallons_used'],
        mpg=data['mpg'],
        engine_miles=data['gallons_used'] * data['mpg']
    )
    db.session.add(trip)
    db.session.commit()
    return jsonify({"message": "Trip added successfully!"})
