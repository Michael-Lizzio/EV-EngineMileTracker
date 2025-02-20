from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    odometer_start = db.Column(db.Integer, nullable=False)
    odometer_end = db.Column(db.Integer, nullable=False)
    gallons_used = db.Column(db.Float, nullable=False)
    mpg = db.Column(db.Float, nullable=False)
    engine_miles = db.Column(db.Float, nullable=False)
