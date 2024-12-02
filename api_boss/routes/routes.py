from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from logger.logger_base import Logger
from flasgger import swag_from

# Define routes for managing bosses (add, update, delete, etc.)
class BossRoutes(Blueprint):
    def __init__(self, boss_service, boss_schema):
        super().__init__('boss', __name__)  # Initialize the Blueprint
        self.boss_service = boss_service  # Service to handle database operations
        self.boss_schema = boss_schema  # Schema to validate the boss data
        self.register_routes()  # Register the routes (endpoints)
        self.logger = Logger()  # Logger for logging messages
        
    def register_routes(self):
        # Register the HTTP routes for the boss API
        self.route('/api/v1/bosses', methods=['GET'])(self.get_bosses)
        self.route('/api/v1/bosses', methods=['POST'])(self.add_bosses)
        self.route('/api/v1/bosses/<int:boss_id>', methods=['PUT'])(self.update_boss)
        self.route('/api/v1/bosses/<int:boss_id>', methods=['DELETE'])(self.delete_boss)
        self.route('/healthcheck', methods=['GET'])(self.healthcheck)

    @swag_from({
        'tags': ['Bosses'],  # API Documentation: Shows this route is for bosses
        'responses': {
            200: {'description': 'List of bosses'},
            500: {'description': 'Internal server error'}
        }
    })
    def get_bosses(self):
        # Get all bosses from the database
        bosses = self.boss_service.get_all_bosses()
        return jsonify(bosses), 200  # Return the list of bosses as JSON
    
    @swag_from({
        'tags': ['Bosses'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string'},
                        'type': {'type': 'string'},
                        'cr': {'type': 'string'},
                        'hp': {'type': 'string'},
                        'ac': {'type': 'string'},
                        'resistances': {'type': 'string'},
                        'inmunities': {'type': 'string'},
                        'abilities': {'type': 'string'},
                    },
                    'required': ['name', 'type', 'cr', 'hp', 'ac', 'resistances', "inmunities", "abilities"]  # These fields are required
                }
            }
        ],
        'responses': {
            201: {'description': 'Boss successfully created'},
            400: {'description': 'Invalid data'},
            500: {'description': 'Internal server error'}
        }
    })
    def add_bosses(self):
        # Add a new boss
        try:
            request_data = request.json  # Get the data from the request

            if not request_data:
                return jsonify({'error': 'Invalid data, empty'}), 400  # Check if data is empty

            name = request_data.get('name')
            type = request_data.get('type')
            cr = request_data.get('cr')
            hp = request_data.get('hp')
            ac = request_data.get('ac')
            resistances = request_data.get('resistances')
            immunities = request_data.get('immunities')
            abilities = request_data.get('abilities')


            # Validate the data using the schema
            try:
                self.boss_schema.validate_name(name)
                self.boss_schema.validate_type(type)
                self.boss_schema.validate_cr(cr)
                self.boss_schema.validate_hp(hp)
                self.boss_schema.validate_ac(ac)
                self.boss_schema.validate_resistances(resistances)
                self.boss_schema.validate_immunities(immunities)
                self.boss_schema.validate_abilities(abilities)

            except ValidationError as e:
                return jsonify({'error': f'Invalid data: {e}'}), 400  # Return error if validation fails

            # Create the new boss object
            new_boss = {
                'name': name,
                'type' : type,
                'cr' : cr,
                'hp' : hp,
                'ac' : ac,
                'resistances' : resistances,
                'immunities' : immunities,
                'abilities' : abilities,
            }
            created_boss = self.boss_service.add_boss(new_boss)  # Add the boss to the database
            self.logger.info(f'New boss: {created_boss}')  # Log the new boss creation
            return jsonify(created_boss), 201  # Return the created boss as JSON
            
        except Exception as e:
            self.logger.error(f'Error adding a new boss to the database: {e}')
            return jsonify({'error': f'An error has occurred: {e}'}), 500  # Handle any errors

    @swag_from({
        'tags': ['Bosses'],
        'parameters': [
            {
                'name': 'boss_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID of the boss to update'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string'},
                        'type': {'type': 'string'},
                        'cr': {'type': 'string'},
                        'hp': {'type': 'string'},
                        'ac': {'type': 'string'},
                        'resistances': {'type': 'string'},
                        'inmunities': {'type': 'string'},
                        'abilities': {'type': 'string'},
                    },
                    'required': ['name', 'type', 'cr', 'hp', 'ac', 'resistances', "inmunities", "abilities"]  # These fields are required
                }
            }
        ],
        'responses': {
            200: {'description': 'Boss successfully updated'},
            400: {'description': 'Invalid data'},
            404: {'description': 'Boss not found'},
            500: {'description': 'Internal server error'}
        }
    })
    def update_boss(self, boss_id):
        # Update an existing boss
        try:
            request_data = request.json  # Get the updated data

            if not request_data:
                return jsonify({'error': 'Invalid data, empty'}), 400  # Check if data is empty

            name = request_data.get('name')
            type = request_data.get('type')
            cr = request_data.get('cr')
            hp = request_data.get('hp')
            ac = request_data.get('ac')
            resistances = request_data.get('resistances')
            immunities = request_data.get('immunities')
            abilities = request_data.get('abilities')


            # Validate the data using the schema
            try:
                self.boss_schema.validate_name(name)
                self.boss_schema.validate_type(type)
                self.boss_schema.validate_cr(cr)
                self.boss_schema.validate_hp(hp)
                self.boss_schema.validate_ac(ac)
                self.boss_schema.validate_resistances(resistances)
                self.boss_schema.validate_immunities(immunities)
                self.boss_schema.validate_abilities(abilities)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data: {e}'}), 400  # Return error if validation fails

            # Update the boss object
            update_boss = {
                '_id' : boss_id,
                'name': name,
                'type' : type,
                'cr' : cr,
                'hp' : hp,
                'ac' : ac,
                'resistances' : resistances,
                'immunities' : immunities,
                'abilities' : abilities,
            }
            updated_boss = self.boss_service.update_boss(boss_id, update_boss)  # Update the boss in the database
            if updated_boss:
                return jsonify(update_boss), 200  # Return the updated boss as JSON
            else:
                return jsonify({'error': 'boss not found'}), 404  # If boss not found, return an error
            
        except Exception as e:
            self.logger.error(f'Error updating the boss in the database: {e}')
            return jsonify({'error': f'Error updating the boss in the database: {e}'}), 500  # Handle any errors

    @swag_from({
        'tags': ['Bosses'],
        'parameters': [
            {
                'name': 'boss_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID of the boss to delete'
            }
        ],
        'responses': {
            200: {'description': 'Boss successfully deleted'},
            404: {'description': 'Boss not found'},
            500: {'description': 'Internal server error'}
        }
    })
    def delete_boss(self, boss_id):
        # Delete a boss by its ID
        try:
            deleted_boss = self.boss_service.delete_boss(boss_id)  # Delete the boss from the database
            
            if deleted_boss:
                return jsonify(deleted_boss), 200  # Return the deleted boss as JSON
            else:
                return jsonify({'error': 'Boss not found'}), 404  # If boss not found, return an error
            
        except Exception as e:
            self.logger.error(f'Error deleting the boss from the database: {e}')
            return jsonify({'error': f'Error deleting the boss from the database: {e}'}), 500  # Handle any errors
        
    @swag_from({
        'tags': ['Health'],
        'responses': {
            200: {'description': 'Server is up'}
        }
    })
    def healthcheck(self):
        # Health check to verify the server is up
        return jsonify({'status': 'up'}), 200
