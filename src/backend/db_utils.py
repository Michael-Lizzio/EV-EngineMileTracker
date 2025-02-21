from flask import Flask
from src.backend.models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///engine_miles.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

def build_db():
    """Builds the database tables if they do not exist."""
    with app.app_context():
        db.create_all()
        print("Database has been built successfully!")

def rebuild_db():
    """Drops all tables and recreates them from models.py (WARNING: This deletes all data!)."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database has been rebuilt successfully!")

# Flask CLI command to build the database
@app.cli.command("build-db")
def build_db_command():
    """Run this command to build the database from scratch."""
    build_db()

# Flask CLI command to rebuild the database
@app.cli.command("rebuild-db")
def rebuild_db_command():
    """Run this command to drop & recreate the database (WARNING: All data will be erased!)."""
    rebuild_db()
