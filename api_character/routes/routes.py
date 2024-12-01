from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from logger.logger_base import Logger
from flasgger import swag_from

# Define routes for managing characters (add, update, delete, etc.)
class CharacterRoutes(Blueprint):
    def __init__(self, character_service, character_schema):
        super().__init__('character', __name__)  # Initialize the Blueprint
        self.character_service = character_service  # Service to handle database operations
        self.character_schema = character_schema  # Schema to validate the character data
        self.register_routes()  # Register the routes (endpoints)
        self.logger = Logger()  # Logger for logging messages
        
    def register_routes(self):
        # Register the HTTP routes for the character API
        self.route('/api/v1/characters', methods=['GET'])(self.get_characters)
        self.route('/api/v1/characters', methods=['POST'])(self.add_characters)
        self.route('/api/v1/characters/<int:character_id>', methods=['PUT'])(self.update_character)
        self.route('/api/v1/characters/<int:character_id>', methods=['DELETE'])(self.delete_character)
        self.route('/healthcheck', methods=['GET'])(self.healthcheck)

    @swag_from({
        'tags': ['Characters'],  # API Documentation: Shows this route is for characters
        'responses': {
            200: {'description': 'List of characters'},
            500: {'description': 'Internal server error'}
        }
    })
    def get_characters(self):
        # Get all characters from the database
        characters = self.character_service.get_all_characters()
        return jsonify(characters), 200  # Return the list of characters as JSON
    
    @swag_from({
        'tags': ['Characters'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'characterName': {'type': 'string'},
                        'race': {'type': 'string'},
                        'className': {'type': 'string'},
                        'alignment': {'type': 'string'},
                        'level': {'type': 'string'},
                        'background': {'type': 'string'},
                        'playerName': {'type': 'string'},
                    },
                    'required': ['characterName', 'race', 'className', 'alignment', 'level', 'background', 'playerName']  # These fields are required
                }
            }
        ],
        'responses': {
            201: {'description': 'Character successfully created'},
            400: {'description': 'Invalid data'},
            500: {'description': 'Internal server error'}
        }
    })
    def add_characters(self):
        # Add a new character
        try:
            request_data = request.json  # Get the data from the request

            if not request_data:
                return jsonify({'error': 'Invalid data, empty'}), 400  # Check if data is empty
                
            characterName = request_data.get('characterName')
            race = request_data.get('race')
            className = request_data.get('className')
            alignment = request_data.get('alignment')
            level = request_data.get('level')
            background = request_data.get('background')
            playerName = request_data.get('playerName')

            # Validate the data using the schema
            try:
                self.character_schema.validate_characterName(characterName)
                self.character_schema.validate_race(race)
                self.character_schema.validate_className(className)
                self.character_schema.validate_alignment(alignment)
                self.character_schema.validate_level(level)
                self.character_schema.validate_background(background)
                self.character_schema.validate_playerName(playerName)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data: {e}'}), 400  # Return error if validation fails

            # Create the new character object
            new_character = {
                'characterName': characterName,
                'race': race,
                'className': className,
                'alignment': alignment,
                'level': level,
                'background': background,
                'playerName': playerName,
            }
            created_character = self.character_service.add_character(new_character)  # Add the character to the database
            self.logger.info(f'New character: {created_character}')  # Log the new character creation
            return jsonify(created_character), 201  # Return the created character as JSON
            
        except Exception as e:
            self.logger.error(f'Error adding a new character to the database: {e}')
            return jsonify({'error': f'An error has occurred: {e}'}), 500  # Handle any errors

    @swag_from({
        'tags': ['Characters'],
        'parameters': [
            {
                'name': 'character_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID of the character to update'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'characterName': {'type': 'string'},
                        'race': {'type': 'string'},
                        'className': {'type': 'string'},
                        'alignment': {'type': 'string'},
                        'level': {'type': 'string'},
                        'background': {'type': 'string'},
                        'playerName': {'type': 'string'},
                    },
                    'required': ['characterName', 'race', 'className', 'alignment', 'level', 'background', 'playerName']  # These fields are required
                }
            }
        ],
        'responses': {
            200: {'description': 'Character successfully updated'},
            400: {'description': 'Invalid data'},
            404: {'description': 'Character not found'},
            500: {'description': 'Internal server error'}
        }
    })
    def update_character(self, character_id):
        # Update an existing character
        try:
            request_data = request.json  # Get the updated data

            if not request_data:
                return jsonify({'error': 'Invalid data, empty'}), 400  # Check if data is empty

            characterName = request_data.get('characterName')
            race = request_data.get('race')
            className = request_data.get('className')
            alignment = request_data.get('alignment')
            level = request_data.get('level')
            background = request_data.get('background')
            playerName = request_data.get('playerName')

            # Validate the data
            try:
                self.character_schema.validate_characterName(characterName)
                self.character_schema.validate_race(race)
                self.character_schema.validate_className(className)
                self.character_schema.validate_alignment(alignment)
                self.character_schema.validate_level(level)
                self.character_schema.validate_background(background)
                self.character_schema.validate_playerName(playerName)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data: {e}'}), 400  # Return error if validation fails

            # Update the character object
            update_character = {
                '_id': character_id,
                'characterName': characterName,
                'race': race,
                'className': className,
                'alignment': alignment,
                'level': level,
                'background': background,
                'playerName': playerName,
            }
            updated_character = self.character_service.update_character(character_id, update_character)  # Update the character in the database
            if updated_character:
                return jsonify(update_character), 200  # Return the updated character as JSON
            else:
                return jsonify({'error': 'Character not found'}), 404  # If character not found, return an error
            
        except Exception as e:
            self.logger.error(f'Error updating the character in the database: {e}')
            return jsonify({'error': f'Error updating the character in the database: {e}'}), 500  # Handle any errors

    @swag_from({
        'tags': ['Characters'],
        'parameters': [
            {
                'name': 'character_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID of the character to delete'
            }
        ],
        'responses': {
            200: {'description': 'Character successfully deleted'},
            404: {'description': 'Character not found'},
            500: {'description': 'Internal server error'}
        }
    })
    def delete_character(self, character_id):
        # Delete a character by its ID
        try:
            deleted_character = self.character_service.delete_character(character_id)  # Delete the character from the database
            
            if deleted_character:
                return jsonify(deleted_character), 200  # Return the deleted character as JSON
            else:
                return jsonify({'error': 'Character not found'}), 404  # If character not found, return an error
            
        except Exception as e:
            self.logger.error(f'Error deleting the character from the database: {e}')
            return jsonify({'error': f'Error deleting the character from the database: {e}'}), 500  # Handle any errors
        
    @swag_from({
        'tags': ['Health'],
        'responses': {
            200: {'description': 'Server is up'}
        }
    })
    def healthcheck(self):
        # Health check to verify the server is up
        return jsonify({'status': 'up'}), 200