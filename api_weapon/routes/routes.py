from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from logger.logger_base import Logger
from flasgger import swag_from

# Define routes for managing weapons (add, update, delete, etc.)
class WeaponRoutes(Blueprint):
    def __init__(self, weapon_service, weapon_schema):
        super().__init__('weapon', __name__)  # Initialize the Blueprint
        self.weapon_service = weapon_service  # Service to handle database operations
        self.weapon_schema = weapon_schema  # Schema to validate the weapon data
        self.register_routes()  # Register the routes (endpoints)
        self.logger = Logger()  # Logger for logging messages
        
    def register_routes(self):
        # Register the HTTP routes for the weapon API
        self.route('/api/v1/weapons', methods=['GET'])(self.get_weapons)
        self.route('/api/v1/weapons', methods=['POST'])(self.add_weapons)
        self.route('/api/v1/weapons/<int:weapon_id>', methods=['PUT'])(self.update_weapon)
        self.route('/api/v1/weapons/<int:weapon_id>', methods=['DELETE'])(self.delete_weapon)
        self.route('/healthcheck', methods=['GET'])(self.healthcheck)

    @swag_from({
        'tags': ['weapons'],  # API Documentation: Shows this route is for weapons
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'named': {'type': 'string'},
                        'category': {'type': 'string'},
                        'cost': {'type': 'string'},
                        'damage': {'type': 'string'},
                        'properties': {'type': 'string'},
                        'description': {'type': 'string'},
                        'weight': {'type': 'string'},
                    },
                    'required': ['named', 'category', 'cost', 'damage', 'properties', 'description', 'weight']  # These fields are required
                }
            }
        ],
        'responses': {
            200: {'description': 'Weapon successfully created'},
            400: {'description': 'Invalid data'},
            500: {'description': 'Internal server error'}
        }
    })
    def get_weapons(self):
        # Get all weapons from the database
        weapons = self.weapon_service.get_all_weapons()
        return jsonify(weapons), 200  # Return the list of weapons as JSON
    
    def add_weapons(self):
        # Add a new weapon
        try:
            request_data = request.json  # Get the data from the request

            if not request_data:
                return jsonify({'error': 'Invalid data, empty'}), 400  # Check if data is empty

            named = request_data.get('named')
            category = request_data.get('category')
            description = request_data.get('description')
            damage = request_data.get('damage')
            properties = request_data.get('properties')
            cost = request_data.get('cost')
            weight = request_data.get('weight')

            # Validate the data using the schema
            try:
                self.weapon_schema.validate_named(named)
                self.weapon_schema.validate_category(category)
                self.weapon_schema.validate_cost(cost)
                self.weapon_schema.validate_properties(properties)
                self.weapon_schema.validate_description(description)
                self.weapon_schema.validate_damage(damage)
                self.weapon_schema.validate_weight(weight)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data: {e}'}), 400  # Return error if validation fails

            # Create the new weapon object
            new_weapon = {
                'named': named,
                'category': category,
                'cost': cost,
                'damage': damage,
                'properties': properties,
                'description': description,
                'weight': weight,
            }
            created_weapon = self.weapon_service.add_weapon(new_weapon)  # Add the weapon to the database
            self.logger.info(f'New weapon: {created_weapon}')  # Log the new weapon creation
            return jsonify(created_weapon), 201  # Return the created weapon as JSON
            
        except Exception as e:
            self.logger.error(f'Error adding a new weapon to the database: {e}')
            return jsonify({'error': f'An error has occurred: {e}'}), 500  # Handle any errors

    def update_weapon(self, weapon_id):
        # Update an existing weapon
        try:
            request_data = request.json  # Get the updated data

            if not request_data:
                return jsonify({'error': 'Invalid data, empty'}), 400  # Check if data is empty

            named = request_data.get('named')
            category = request_data.get('category')
            cost = request_data.get('cost')
            damage = request_data.get('damage')
            properties = request_data.get('properties')
            description = request_data.get('description')
            weight = request_data.get('weight')

            # Validate the data
            try:
                self.weapon_schema.validate_named(named)
                self.weapon_schema.validate_category(category)
                self.weapon_schema.validate_description(description)
                self.weapon_schema.validate_damage(damage)
                self.weapon_schema.validate_properties(properties)
                self.weapon_schema.validate_cost(cost)
                self.weapon_schema.validate_weight(weight)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data: {e}'}), 400  # Return error if validation fails

            # Update the weapon object
            update_weapon = {
                '_id': weapon_id,
                'named': named,
                'category': category,
                'cost': cost,
                'damage': damage,
                'properties': properties,
                'description': description,
                'weight': weight,
            }
            updated_weapon = self.weapon_service.update_weapon(weapon_id, update_weapon)  # Update the weapon in the database
            if updated_weapon:
                return jsonify(update_weapon), 200  # Return the updated weapon as JSON
            else:
                return jsonify({'error': 'Weapon not found'}), 404  # If weapon not found, return an error
            
        except Exception as e:
            self.logger.error(f'Error updating the weapon in the database: {e}')
            return jsonify({'error': f'Error updating the weapon in the database: {e}'}), 500  # Handle any errors

    def delete_weapon(self, weapon_id):
        # Delete a weapon by its ID
        try:
            deleted_weapon = self.weapon_service.delete_weapon(weapon_id)  # Delete the weapon from the database
            
            if deleted_weapon:
                return jsonify(deleted_weapon), 200  # Return the deleted weapon as JSON
            else:
                return jsonify({'error': 'Weapon not found'}), 404  # If weapon not found, return an error
            
        except Exception as e:
            self.logger.error(f'Error deleting the weapon from the database: {e}')
            return jsonify({'error': f'Error deleting the weapon from the database: {e}'}), 500  # Handle any errors
        
    def healthcheck(self):
        # Health check to verify the server is up
        return jsonify({'status': 'up'}), 200
