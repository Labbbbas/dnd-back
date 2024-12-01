# Import necessary modules
from flask import Flask

from models.models import WeaponModel  # Import the model to interact with the database
from services.services import WeaponService  # Import the service to handle business logic
from schemas.schemas import WeaponSchema  # Import the schema for data validation
from routes.routes import WeaponRoutes  # Import the routes to manage the API endpoints
from flasgger import Swagger  # Import Swagger for API documentation

from flask_cors import CORS  # Import CORS to handle cross-origin requests

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for the app

# Set up Swagger for automatic API documentation
swagger = Swagger(app)

# Initialize the database connection
db_conn = WeaponModel()
db_conn.connect_to_database()  # Connect to the database

# Initialize the service with the database connection
weapon_service = WeaponService(db_conn)

# Initialize the schema for data validation
weapon_schema = WeaponSchema()

# Initialize the routes for the API and register them
weapon_routes = WeaponRoutes(weapon_service, weapon_schema)
app.register_blueprint(weapon_routes)  # Register the routes with the Flask app

# Start the Flask app
if __name__ == '__main__':
    try:
        # Run the app in debug mode for development
        app.run(debug=True)
    finally:
        # Close the database connection when the app stops
        db_conn.close_connection()
