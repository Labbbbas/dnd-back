# Import necessary modules
from flask import Flask

from models.models import CampaignModel  # Import the model to interact with the database
from services.services import CampaignService  # Import the service to handle business logic
from schemas.schemas import CampaignSchema  # Import the schema for data validation
from routes.routes import CampaignRoutes  # Import the routes to manage the API endpoints
from flasgger import Swagger  # Import Swagger for API documentation

from flask_cors import CORS  # Import CORS to handle cross-origin requests

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for the app

# Set up Swagger for automatic API documentation
swagger = Swagger(app)

# Initialize the database connection
db_conn = CampaignModel()
db_conn.connect_to_database()  # Connect to the database

# Initialize the service with the database connection
campaign_service = CampaignService(db_conn)

# Initialize the schema for data validation
campaign_schema = CampaignSchema()

# Initialize the routes for the API and register them
campaign_routes = CampaignRoutes(campaign_service, campaign_schema)
app.register_blueprint(campaign_routes)  # Register the routes with the Flask app

# Start the Flask app
if __name__ == '__main__':
    try:
        # Run the app in debug mode for development
        app.run(debug=True, host='0.0.0.0',port=8003)
    finally:
        # Close the database connection when the app stops
        db_conn.close_connection()
