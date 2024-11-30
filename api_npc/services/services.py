# Import necessary modules
from flask import jsonify
from logger.logger_base import Logger

class NpcService:
    def __init__(self, db_conn):
        # Set up logging and database connection
        self.logger = Logger()  # Logger for logging messages
        self.db_conn = db_conn  # Database connection

    def get_all_npcs(self):
        try:
            # Fetch all npcs from the database and return them as a list
            npcs = list(self.db_conn.db.npcs.find())
            return npcs
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error fetching all npcs from the database: {e}')
            return jsonify({'error': f'Error fetching all npcs from the database: {e}'}), 500

    def add_npc(self, new_npc):
        try:
            # Find the npc with the highest ID and set the new npc ID to be the next one
            max_npc = self.db_conn.db.npcs.find_one(sort=[('_id', -1)])
            next_id = max_npc['_id'] + 1 if max_npc else 1
            new_npc['_id'] = next_id  # Assign new ID to the npc
            self.db_conn.db.npcs.insert_one(new_npc)  # Add the new npc to the database
            return new_npc  # Return the newly added npc
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error creating the new npc: {e}')
            return jsonify({'error': f'Error creating the new npc: {e}'}), 500

    def get_npc_by_id(self, npc_id):
        try:
            # Fetch a specific npc by its ID from the database
            npc_data = self.db_conn.db.npcs.find_one({'_id': npc_id})
            return npc_data  # Return the npc data
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error fetching the npc id from the database {e}')
            return jsonify({'error': f'Error fetching the npc id from the database: {e}'}), 500
        
    def update_npc(self, npc_id, npc_data):
        try:
            # First, check if the npc exists
            update_npc = self.get_npc_by_id(npc_id)

            if update_npc:
                # If the npc exists, update it with the new data
                updated_npc = self.db_conn.db.npcs.update_one({'_id': npc_id}, {'$set': npc_data})
                if updated_npc.modified_count > 0:
                    return updated_npc  # Return the updated npc
                else:
                    return 'The npc is already up-to-date'  # No changes made
            else:
                return None  # npc not found
            
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error updating the npc: {e}')
            return jsonify({'error': f'Error updating the npc: {e}'}), 500
        
    def delete_npc(self, npc_id):
        try:
            # Check if the npc exists before deleting
            deleted_npc = self.get_npc_by_id(npc_id)
            
            if deleted_npc:
                # If the npc exists, delete it from the database
                self.db_conn.db.npcs.delete_one({'_id': npc_id})
                return deleted_npc  # Return the deleted npc data
            else:
                return None  # npc not found
            
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error deleting the npc data: {e}')
            return jsonify({'error': f'Error deleting the npc data: {e}'}), 500

# Main block of code for testing the NpcService
if __name__ == '__main__':
    from models.models import NpcModel
    
    logger = Logger()  # Logger for logging messages
    db_conn = NpcModel()  # Database connection
    npc_service = NpcService(db_conn)  # Creating the service with the database connection
    
    try:
        db_conn.connect_to_database()  # Connect to the database
        
        # Fetch all npcs and log the result
        npcs = npc_service.get_all_npcs()
        logger.info(f'Npcs fetched: {npcs}')
        
        # Example operations (currently commented out):
        # Add a new npc
        # new_npc = npc_service.add_npc({'role': 'Nahual'})
        # logger.info(f'New npc added: {new_npc}')
        
        # Get a npc by its ID
        # npc_data = npc_service.get_npc_by_id(3)
        # logger.info(f'npc: {npc_data}')
        
        # Update a npc
        # updated_npc = npc_service.update_npc(6, {'author': 'H.P. Lovecraft'})
        # logger.info(f'Updated npc: {updated_npc}')
        
        # Delete a npc
        # deleted_npc = npc_service.delete_npc(6)
        # logger.info(f'Deleted npc: {deleted_npc}')
        
    except Exception as e:
        # If something goes wrong, log the error
        logger.error(f'An error has occurred: {e}')
    finally:
        db_conn.close_connection()  # Close the database connection
        logger.info('Connection to database closed')  # Log that the connection is closed
