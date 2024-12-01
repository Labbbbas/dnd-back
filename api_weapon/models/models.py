import os  # Import the os module to access environment variables
from logger.logger_base import Logger  # Import the custom Logger class
from pymongo import MongoClient  # Import MongoClient to interact with MongoDB

class WeaponModel:  # Class ToolWeaponModel
    def __init__(self):
        # Initialize the MongoDB client and database variables
        self.client = None
        self.db = None
        self.logger = Logger()  # Initialize the Logger instance
    
    def connect_to_database(self):
        # Retrieve MongoDB credentials from environment variables
        mongodb_user = os.environ.get('MONGODB_USER')  # MongoDB username
        mongodb_pass = os.environ.get('MONGODB_PASS')  # MongoDB password
        mongodb_host = os.environ.get('MONGODB_HOST')  # MongoDB host address
        
        # Validate that all necessary environment variables are set
        if not mongodb_user or not mongodb_pass or not mongodb_host:
            self.logger.critical('MongoDB environment variables are required')  # Log critical error
            raise ValueError('Set environment MONGODB_USER, MONGODB_PASS, MONGODB_HOST')  # Raise an exception
        
        try:
            # Attempt to connect to MongoDB using the provided credentials
            self.client = MongoClient(
                host=mongodb_host,  # MongoDB host
                port=27017,  # MongoDB default port
                username=mongodb_user,  # MongoDB username
                password=mongodb_pass,  # MongoDB password
                authSource='admin',  # Authentication source
                authMechanism='SCRAM-SHA-256',  # Authentication mechanism
                serverSelectionTimeoutMS=5000  # Timeout for server selection
            )
            self.db = self.client['microservices']  # Connect to the 'microservices' database
            # Check if the database has collections to confirm connection
            if self.db.list_collection_names():
                self.logger.info('Connected to MongoDB database successfully')  # Log successful connection
        except Exception as e:
            # Log critical error and raise an exception if the connection fails
            self.logger.critical(f'Failed to connect to the database: {e}')
            raise
        
    def close_connection(self):
        # Close the MongoDB connection if it exists
        if self.client:
            self.client.close()  # Close the client connection


if __name__ == '__main__':
    db_conn = ToolWeaponModel()  # Create an instance of ToolWeaponModel
    logger = Logger()  # Create an instance of the Logger
    
    try:
        # Try to connect to the MongoDB database
        db_conn.connect_to_database()
    except Exception as e:
        # Log a critical error if an exception occurs
        logger.critical(f'An error occurred: {e}')
    finally:
        # Ensure the connection is closed in all cases
        db_conn.close_connection()
        logger.info('Connection to the database was successfully closed')  # Log successful closure
