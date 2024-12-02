# Import necessary modules
from flask import Flask

from models.models import BossModel  # Import the model to interact with the database
from services.services import BossService  # Import the service to handle business logic
from schemas.schemas import BossSchema  # Import the schema for data validation
from routes.routes import BossRoutes  # Import the routes to manage the API endpoints
from flasgger import Swagger  # Import Swagger for API documentation

from flask_cors import CORS  # Import CORS to handle cross-origin requests

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for the app

# Set up Swagger for automatic API documentation
swagger = Swagger(app)

# Initialize the database connection
db_conn = BossModel()
db_conn.connect_to_database()  # Connect to the database

# Initialize the service with the database connection
boss_service = BossService(db_conn)

# Initialize the schema for data validation
boss_schema = BossSchema()

# Initialize the routes for the API and register them
boss_routes = BossRoutes(boss_service, boss_schema)
app.register_blueprint(boss_routes)  # Register the routes with the Flask app

# Start the Flask app
if __name__ == '__main__':
    try:
        # Run the app in debug mode for development
        app.run(debug=True)
    finally:
        # Close the database connection when the app stops
        db_conn.close_connection()
