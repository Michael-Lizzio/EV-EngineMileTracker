from flask import Flask
from src.routes import app as routes_app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///engine_miles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Register routes
app.register_blueprint(routes_app)

if __name__ == "__main__":
    app.run(debug=True)
