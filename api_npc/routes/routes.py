from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from logger.logger_base import Logger
from flasgger import swag_from

# Define routes for managing npcs (add, update, delete, etc.)
class NpcRoutes(Blueprint):
    def __init__(self, npc_service, npc_schema):
        super().__init__('npc', __name__)  # Initialize the Blueprint
        self.npc_service = npc_service  # Service to handle database operations
        self.npc_schema = npc_schema  # Schema to validate the npc data
        self.register_routes()  # Register the routes (endpoints)
        self.logger = Logger()  # Logger for logging messages
        
    def register_routes(self):
        # Register the HTTP routes for the npc API
        self.route('/api/v1/npcs', methods=['GET'])(self.get_npcs)
        self.route('/api/v1/npcs', methods=['POST'])(self.add_npcs)
        self.route('/api/v1/npcs/<int:npc_id>', methods=['PUT'])(self.update_npc)
        self.route('/api/v1/npcs/<int:npc_id>', methods=['DELETE'])(self.delete_npc)
        self.route('/healthcheck', methods=['GET'])(self.healthcheck)

    @swag_from({
        'tags': ['Npcs'],  # API Documentation: Shows this route is for npcs
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'named': {'type': 'string'},
                        'role': {'type': 'string'},
                        'personality': {'type': 'string'},
                        'inventory': {'type': 'string'},
                        'likes': {'type': 'string'},
                        'money': {'type': 'string'},
                    },
                    'required': ['named', 'role', 'personality', 'inventory', 'likes', 'money']  # These fields are required
                }
            }
        ],
        'responses': {
            200: {'description': 'Npc successfully created'},
            400: {'description': 'Invalid data'},
            500: {'description': 'Internal server error'}
        }
    })
    def get_npcs(self):
        # Get all npcs from the database
        npcs = self.npc_service.get_all_npcs()
        return jsonify(npcs), 200  # Return the list of npcs as JSON
    
    def add_npcs(self):
        # Add a new npc
        try:
            request_data = request.json  # Get the data from the request

            if not request_data:
                return jsonify({'error': 'Invalid data, empty'}), 400  # Check if data is empty

            named = request_data.get('named')
            role = request_data.get('role')
            personality = request_data.get('personality')
            inventory = request_data.get('inventory')
            likes = request_data.get('likes')
            money = request_data.get('money')

            # Validate the data using the schema
            try:
                self.npc_schema.validate_named(named)
                self.npc_schema.validate_role(role)
                self.npc_schema.validate_personality(personality)
                self.npc_schema.validate_inventory(inventory)
                self.npc_schema.validate_likes(likes)
                self.npc_schema.validate_money(money)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data: {e}'}), 400  # Return error if validation fails

            # Create the new npc object
            new_npc = {
                'named': named,
                'role': role,
                'personality': personality,
                'inventory': inventory,
                'likes': likes,
                'money': money,
            }
            created_npc = self.npc_service.add_npc(new_npc)  # Add the npc to the database
            self.logger.info(f'New npc: {created_npc}')  # Log the new npc creation
            return jsonify(created_npc), 201  # Return the created npc as JSON
            
        except Exception as e:
            self.logger.error(f'Error adding a new npc to the database: {e}')
            return jsonify({'error': f'An error has occurred: {e}'}), 500  # Handle any errors

    def update_npc(self, npc_id):
        # Update an existing npc
        try:
            request_data = request.json  # Get the updated data

            if not request_data:
                return jsonify({'error': 'Invalid data, empty'}), 400  # Check if data is empty

            named = request_data.get('named')
            role = request_data.get('role')
            personality = request_data.get('personality')
            inventory = request_data.get('inventory')
            likes = request_data.get('likes')
            money = request_data.get('money')

            # Validate the data
            try:
                self.npc_schema.validate_named(named)
                self.npc_schema.validate_role(role)
                self.npc_schema.validate_personality(personality)
                self.npc_schema.validate_inventory(inventory)
                self.npc_schema.validate_likes(likes)
                self.npc_schema.validate_money(money)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data: {e}'}), 400  # Return error if validation fails

            # Update the npc object
            update_npc = {
                '_id': npc_id,
                'named': named,
                'role': role,
                'personality': personality,
                'inventory': inventory,
                'likes': likes,
                'money': money,
            }
            updated_npc = self.npc_service.update_npc(npc_id, update_npc)  # Update the npc in the database
            if updated_npc:
                return jsonify(update_npc), 200  # Return the updated npc as JSON
            else:
                return jsonify({'error': 'Npc not found'}), 404  # If npc not found, return an error
            
        except Exception as e:
            self.logger.error(f'Error updating the npc in the database: {e}')
            return jsonify({'error': f'Error updating the npc in the database: {e}'}), 500  # Handle any errors

    def delete_npc(self, npc_id):
        # Delete a npc by its ID
        try:
            deleted_npc = self.npc_service.delete_npc(npc_id)  # Delete the npc from the database
            
            if deleted_npc:
                return jsonify(deleted_npc), 200  # Return the deleted npc as JSON
            else:
                return jsonify({'error': 'Npc not found'}), 404  # If npc not found, return an error
            
        except Exception as e:
            self.logger.error(f'Error deleting the npc from the database: {e}')
            return jsonify({'error': f'Error deleting the npc from the database: {e}'}), 500  # Handle any errors
        
    def healthcheck(self):
        # Health check to verify the server is up
        return jsonify({'status': 'up'}), 200
