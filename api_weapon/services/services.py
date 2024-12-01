# Import necessary modules
from flask import jsonify
from logger.logger_base import Logger

class WeaponService:
    def __init__(self, db_conn):
        # Set up logging and database connection
        self.logger = Logger()  # Logger for logging messages
        self.db_conn = db_conn  # Database connection

    def get_all_weapons(self):
        try:
            # Fetch all weapons from the database and return them as a list
            weapons = list(self.db_conn.db.weapons.find())
            return weapons
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error fetching all weapons from the database: {e}')
            return jsonify({'error': f'Error fetching all weapons from the database: {e}'}), 500

    def add_weapon(self, new_weapon):
        try:
            # Find the weapon with the highest ID and set the new weapon ID to be the next one
            max_weapon = self.db_conn.db.weapons.find_one(sort=[('_id', -1)])
            next_id = max_weapon['_id'] + 1 if max_weapon else 1
            new_weapon['_id'] = next_id  # Assign new ID to the weapon
            self.db_conn.db.weapons.insert_one(new_weapon)  # Add the new weapon to the database
            return new_weapon  # Return the newly added weapon
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error creating the new weapon: {e}')
            return jsonify({'error': f'Error creating the new weapon: {e}'}), 500

    def get_weapon_by_id(self, weapon_id):
        try:
            # Fetch a specific weapon by its ID from the database
            weapon_data = self.db_conn.db.weapons.find_one({'_id': weapon_id})
            return weapon_data  # Return the weapon data
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error fetching the weapon id from the database {e}')
            return jsonify({'error': f'Error fetching the weapon id from the database: {e}'}), 500
        
    def update_weapon(self, weapon_id, weapon_data):
        try:
            # First, check if the weapon exists
            update_weapon = self.get_weapon_by_id(weapon_id)

            if update_weapon:
                # If the weapon exists, update it with the new data
                updated_weapon = self.db_conn.db.weapons.update_one({'_id': weapon_id}, {'$set': weapon_data})
                if updated_weapon.modified_count > 0:
                    return updated_weapon  # Return the updated weapon
                else:
                    return 'The weapon is already up-to-date'  # No changes made
            else:
                return None  # Weapon not found
            
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error updating the weapon: {e}')
            return jsonify({'error': f'Error updating the weapon: {e}'}), 500
        
    def delete_weapon(self, weapon_id):
        try:
            # Check if the weapon exists before deleting
            deleted_weapon = self.get_weapon_by_id(weapon_id)
            
            if deleted_weapon:
                # If the weapon exists, delete it from the database
                self.db_conn.db.weapons.delete_one({'_id': weapon_id})
                return deleted_weapon  # Return the deleted weapon data
            else:
                return None  # Weapon not found
            
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error deleting the weapon data: {e}')
            return jsonify({'error': f'Error deleting the weapon data: {e}'}), 500

# Main block of code for testing the WeaponService
if __name__ == '__main__':
    from models.models import WeaponModel
    
    logger = Logger()  # Logger for logging messages
    db_conn = WeaponModel()  # Database connection
    weapon_service = WeaponService(db_conn)  # Creating the service with the database connection
    
    try:
        db_conn.connect_to_database()  # Connect to the database
        
        # Fetch all weapons and log the result
        weapons = weapon_service.get_all_weapons()
        logger.info(f'Weapons fetched: {weapons}')
        
        # Example operations (currently commented out):
        # Add a new weapon
        # new_weapon = weapon_service.add_weapon({'role': 'Nahual'})
        # logger.info(f'New weapon added: {new_weapon}')
        
        # Get a weapon by its ID
        # weapon_data = weapon_service.get_weapon_by_id(3)
        # logger.info(f'weapon: {weapon_data}')
        
        # Update a weapon
        # updated_weapon = weapon_service.update_weapon(6, {'author': 'H.P. Lovecraft'})
        # logger.info(f'Updated Weapon: {updated_weapon}')
        
        # Delete a weapon
        # deleted_weapon = weapon_service.delete_weapon(6)
        # logger.info(f'Deleted Weapon: {deleted_weapon}')
        
    except Exception as e:
        # If something goes wrong, log the error
        logger.error(f'An error has occurred: {e}')
    finally:
        db_conn.close_connection()  # Close the database connection
        logger.info('Connection to database closed')  # Log that the connection is closed
