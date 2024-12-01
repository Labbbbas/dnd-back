# Import necessary modules
from flask import jsonify
from logger.logger_base import Logger

class CharacterService:
    def __init__(self, db_conn):
        # Set up logging and database connection
        self.logger = Logger()  # Logger for logging messages
        self.db_conn = db_conn  # Database connection

    def get_all_characters(self):
        try:
            # Fetch all characters from the database and return them as a list
            characters = list(self.db_conn.db.characters.find())
            return characters
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error fetching all characters from the database: {e}')
            return jsonify({'error': f'Error fetching all characters from the database: {e}'}), 500

    def add_character(self, new_character):
        try:
            # Try to get the highest ID in the collection
            max_character = self.db_conn.db.characters.find_one(sort=[('_id', -1)])
            # If a character exists, increment its ID by 1; otherwise, start from 1
            next_id = max_character['_id'] + 1 if max_character else 1
            # Assign the new ID to the character
            new_character['_id'] = next_id  
            # Insert the new character into the database
            self.db_conn.db.characters.insert_one(new_character)
            
            # Return the newly added character
            return new_character
    
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error creating the new character: {e}')
            
            # Return a 500 error response with the error message
            return jsonify({'error': f'Error creating the new character: {e}'}), 500

    def get_character_by_id(self, character_id):
        try:
            # Fetch a specific character by its ID from the database
            character_data = self.db_conn.db.characters.find_one({'_id': character_id})
            return character_data  # Return the character data
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error fetching the character id from the database {e}')
            return jsonify({'error': f'Error fetching the character id from the database: {e}'}), 500
        
    def update_character(self, character_id, character_data):
        try:
            # First, check if the character exists
            update_character = self.get_character_by_id(character_id)

            if update_character:
                # If the character exists, update it with the new data
                updated_character = self.db_conn.db.characters.update_one({'_id': character_id}, {'$set': character_data})
                if updated_character.modified_count > 0:
                    return updated_character  # Return the updated character
                else:
                    return 'The character is already up-to-date'  # No changes made
            else:
                return None  # Character not found
            
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error updating the character: {e}')
            return jsonify({'error': f'Error updating the character: {e}'}), 500
        
    def delete_character(self, character_id):
        try:
            # Check if the character exists before deleting
            deleted_character = self.get_character_by_id(character_id)
            
            if deleted_character:
                # If the character exists, delete it from the database
                self.db_conn.db.characters.delete_one({'_id': character_id})
                return deleted_character  # Return the deleted character data
            else:
                return None  # Character not found
            
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error deleting the character data: {e}')
            return jsonify({'error': f'Error deleting the character data: {e}'}), 500

# Main block of code for testing the CharacterService
if __name__ == '__main__':
    from models.models import CharacterModel
    
    logger = Logger()  # Logger for logging messages
    db_conn = CharacterModel()  # Database connection
    character_service = CharacterService(db_conn)  # Creating the service with the database connection
    
    try:
        db_conn.connect_to_database()  # Connect to the database
        
        # Fetch all characters and log the result
        characters = character_service.get_all_characters()
        logger.info(f'Characters fetched: {characters}')
        
    except Exception as e:
        # If something goes wrong, log the error
        logger.error(f'An error has occurred: {e}')
    finally:
        db_conn.close_connection()  # Close the database connection
        logger.info('Connection to database closed')  # Log that the connection is closed
