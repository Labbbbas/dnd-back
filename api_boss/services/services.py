# Import necessary modules
from flask import jsonify
from logger.logger_base import Logger

class BossService:
    def __init__(self, db_conn):
        # Set up logging and database connection
        self.logger = Logger()  # Logger for logging messages
        self.db_conn = db_conn  # Database connection

    def get_all_bosses(self):
        try:
            # Fetch all bosses from the database and return them as a list
            bosses = list(self.db_conn.db.bosses.find())
            return bosses
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error fetching all bosses from the database: {e}')
            return jsonify({'error': f'Error fetching all bosses from the database: {e}'}), 500

    def add_boss(self, new_boss):
        try:
            # Try to get the highest ID in the collection
            max_boss = self.db_conn.db.bosses.find_one(sort=[('_id', -1)])
            # If a boss exists, increment its ID by 1; otherwise, start from 1
            next_id = max_boss['_id'] + 1 if max_boss else 1
            # Assign the new ID to the boss
            new_boss['_id'] = next_id  
            # Insert the new boss into the database
            self.db_conn.db.bosses.insert_one(new_boss)
            
            # Return the newly added boss
            return new_boss
    
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error creating the new boss: {e}')
            
            # Return a 500 error response with the error message
            return jsonify({'error': f'Error creating the new boss: {e}'}), 500

    def get_boss_by_id(self, boss_id):
        try:
            # Fetch a specific boss by its ID from the database
            boss_data = self.db_conn.db.bosses.find_one({'_id': boss_id})
            return boss_data  # Return the boss data
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error fetching the boss id from the database {e}')
            return jsonify({'error': f'Error fetching the boss id from the database: {e}'}), 500
        
    def update_boss(self, boss_id, boss_data):
        try:
            # First, check if the boss exists
            update_boss = self.get_boss_by_id(boss_id)

            if update_boss:
                # If the boss exists, update it with the new data
                updated_boss = self.db_conn.db.bosses.update_one({'_id': boss_id}, {'$set': boss_data})
                if updated_boss.modified_count > 0:
                    return updated_boss  # Return the updated boss
                else:
                    return 'The boss is already up-to-date'  # No changes made
            else:
                return None  # Boss not found
            
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error updating the boss: {e}')
            return jsonify({'error': f'Error updating the boss: {e}'}), 500
        
    def delete_boss(self, boss_id):
        try:
            # Check if the boss exists before deleting
            deleted_boss = self.get_boss_by_id(boss_id)
            
            if deleted_boss:
                # If the boss exists, delete it from the database
                self.db_conn.db.bosses.delete_one({'_id': boss_id})
                return deleted_boss  # Return the deleted boss data
            else:
                return None  # Boss not found
            
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error deleting the boss data: {e}')
            return jsonify({'error': f'Error deleting the boss data: {e}'}), 500

# Main block of code for testing the BossService
if __name__ == '__main__':
    from models.models import BossModel
    
    logger = Logger()  # Logger for logging messages
    db_conn = BossModel()  # Database connection
    boss_service = BossService(db_conn)  # Creating the service with the database connection
    
    try:
        db_conn.connect_to_database()  # Connect to the database
        
        # Fetch all bosses and log the result
        bosses = boss_service.get_all_bosses()
        logger.info(f'Bosses fetched: {bosses}')
        
        # Example operations (currently commented out):
        # Add a new boss
        # new_boss = boss_service.add_boss({'role': 'Nahual'})
        # logger.info(f'New boss added: {new_boss}')
        
        # Get a boss by its ID
        # boss_data = boss_service.get_boss_by_id(3)
        # logger.info(f'boss: {boss_data}')
        
        # Update a boss
        # updated_boss = boss_service.update_boss(6, {'author': 'H.P. Lovecraft'})
        # logger.info(f'Updated Boss: {updated_boss}')
        
        # Delete a boss
        # deleted_boss = boss_service.delete_boss(6)
        # logger.info(f'Deleted Boss: {deleted_boss}')
        
    except Exception as e:
        # If something goes wrong, log the error
        logger.error(f'An error has occurred: {e}')
    finally:
        db_conn.close_connection()  # Close the database connection
        logger.info('Connection to database closed')  # Log that the connection is closed
