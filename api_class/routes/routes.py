from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from logger.logger_base import Logger
from flasgger import swag_from

# Define routes for managing classes (add, update, delete, etc.)
class ClassRoutes(Blueprint):
    def __init__(self, class_service, class_schema):
        super().__init__('class', __name__)  # Initialize the Blueprint
        self.class_service = class_service  # Service to handle database operations
        self.class_schema = class_schema  # Schema to validate the class data
        self.register_routes()  # Register the routes (endpoints)
        self.logger = Logger()  # Logger for logging messages
        
    def register_routes(self):
        # Register the HTTP routes for the class API
        self.route('/api/v1/classes', methods=['GET'])(self.get_classes)
        self.route('/api/v1/classes', methods=['POST'])(self.add_classes)
        self.route('/api/v1/classes/<int:class_id>', methods=['PUT'])(self.update_class)
        self.route('/api/v1/classes/<int:class_id>', methods=['DELETE'])(self.delete_class)
        self.route('/healthcheck', methods=['GET'])(self.healthcheck)

    @swag_from({
        'tags': ['Classes'],  # API Documentation: Shows this route is for classes
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'role': {'type': 'string'},
                        'description': {'type': 'string'},
                        'hd': {'type': 'string'},
                        'pa': {'type': 'string'},
                        'stp': {'type': 'string'},
                        'awp': {'type': 'string'},
                    },
                    'required': ['role', 'description', 'hd', 'pa', 'stp', 'awp']  # These fields are required
                }
            }
        ],
        'responses': {
            200: {'description': 'Class successfully created'},
            400: {'description': 'Invalid data'},
            500: {'description': 'Internal server error'}
        }
    })
    def get_classes(self):
        # Get all classes from the database
        classes = self.class_service.get_all_classes()
        return jsonify(classes), 200  # Return the list of classes as JSON
    
    def add_classes(self):
        # Add a new class
        try:
            request_data = request.json  # Get the data from the request

            if not request_data:
                return jsonify({'error': 'Invalid data, empty'}), 400  # Check if data is empty

            role = request_data.get('role')
            description = request_data.get('description')
            hd = request_data.get('hd')
            pa = request_data.get('pa')
            stp = request_data.get('stp')
            awp = request_data.get('awp')

            # Validate the data using the schema
            try:
                self.class_schema.validate_role(role)
                self.class_schema.validate_description(description)
                self.class_schema.validate_hd(hd)
                self.class_schema.validate_pa(pa)
                self.class_schema.validate_stp(stp)
                self.class_schema.validate_awp(awp)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data: {e}'}), 400  # Return error if validation fails

            # Create the new class object
            new_class = {
                'role': role,
                'description': description,
                'hd': hd,
                'pa': pa,
                'stp': stp,
                'awp': awp,
            }
            created_class = self.class_service.add_class(new_class)  # Add the class to the database
            self.logger.info(f'New class: {created_class}')  # Log the new class creation
            return jsonify(created_class), 201  # Return the created class as JSON
            
        except Exception as e:
            self.logger.error(f'Error adding a new class to the database: {e}')
            return jsonify({'error': f'An error has occurred: {e}'}), 500  # Handle any errors

    def update_class(self, class_id):
        # Update an existing class
        try:
            request_data = request.json  # Get the updated data

            if not request_data:
                return jsonify({'error': 'Invalid data, empty'}), 400  # Check if data is empty

            role = request_data.get('role')
            description = request_data.get('description')
            hd = request_data.get('hd')
            pa = request_data.get('pa')
            stp = request_data.get('stp')
            awp = request_data.get('awp')

            # Validate the data
            try:
                self.class_schema.validate_role(role)
                self.class_schema.validate_description(description)
                self.class_schema.validate_hd(hd)
                self.class_schema.validate_pa(pa)
                self.class_schema.validate_stp(stp)
                self.class_schema.validate_awp(awp)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data: {e}'}), 400  # Return error if validation fails

            # Update the class object
            update_class = {
                '_id': class_id,
                'role': role,
                'description': description,
                'hd': hd,
                'pa': pa,
                'stp': stp,
                'awp': awp,
            }
            updated_class = self.class_service.update_class(class_id, update_class)  # Update the class in the database
            if updated_class:
                return jsonify(update_class), 200  # Return the updated class as JSON
            else:
                return jsonify({'error': 'Class not found'}), 404  # If class not found, return an error
            
        except Exception as e:
            self.logger.error(f'Error updating the class in the database: {e}')
            return jsonify({'error': f'Error updating the class in the database: {e}'}), 500  # Handle any errors

    def delete_class(self, class_id):
        # Delete a class by its ID
        try:
            deleted_class = self.class_service.delete_class(class_id)  # Delete the class from the database
            
            if deleted_class:
                return jsonify(deleted_class), 200  # Return the deleted class as JSON
            else:
                return jsonify({'error': 'Class not found'}), 404  # If class not found, return an error
            
        except Exception as e:
            self.logger.error(f'Error deleting the class from the database: {e}')
            return jsonify({'error': f'Error deleting the class from the database: {e}'}), 500  # Handle any errors
        
    def healthcheck(self):
        # Health check to verify the server is up
        return jsonify({'status': 'up'}), 200
