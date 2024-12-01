# Import necessary modules
from flask import jsonify
from logger.logger_base import Logger

class ClassService:
    def __init__(self, db_conn):
        # Set up logging and database connection
        self.logger = Logger()  # Logger for logging messages
        self.db_conn = db_conn  # Database connection

    def get_all_classes(self):
        try:
            # Fetch all classes from the database and return them as a list
            classes = list(self.db_conn.db.classes.find())
            return classes
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error fetching all classes from the database: {e}')
            return jsonify({'error': f'Error fetching all classes from the database: {e}'}), 500

    def add_class(self, new_class):
        try:
            # Try to get the highest ID in the collection
            max_class = self.db_conn.db.classes.find_one(sort=[('_id', -1)])
            # If a class exists, increment its ID by 1; otherwise, start from 1
            next_id = max_class['_id'] + 1 if max_class else 1
            # Assign the new ID to the class
            new_class['_id'] = next_id  
            # Insert the new class into the database
            self.db_conn.db.classes.insert_one(new_class)
            
            # Return the newly added class
            return new_class
    
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error creating the new class: {e}')
            
            # Return a 500 error response with the error message
            return jsonify({'error': f'Error creating the new class: {e}'}), 500

    def get_class_by_id(self, class_id):
        try:
            # Fetch a specific class by its ID from the database
            class_data = self.db_conn.db.classes.find_one({'_id': class_id})
            return class_data  # Return the class data
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error fetching the class id from the database {e}')
            return jsonify({'error': f'Error fetching the class id from the database: {e}'}), 500
        
    def update_class(self, class_id, class_data):
        try:
            # First, check if the class exists
            update_class = self.get_class_by_id(class_id)

            if update_class:
                # If the class exists, update it with the new data
                updated_class = self.db_conn.db.classes.update_one({'_id': class_id}, {'$set': class_data})
                if updated_class.modified_count > 0:
                    return updated_class  # Return the updated class
                else:
                    return 'The class is already up-to-date'  # No changes made
            else:
                return None  # Class not found
            
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error updating the class: {e}')
            return jsonify({'error': f'Error updating the class: {e}'}), 500
        
    def delete_class(self, class_id):
        try:
            # Check if the class exists before deleting
            deleted_class = self.get_class_by_id(class_id)
            
            if deleted_class:
                # If the class exists, delete it from the database
                self.db_conn.db.classes.delete_one({'_id': class_id})
                return deleted_class  # Return the deleted class data
            else:
                return None  # Class not found
            
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error deleting the class data: {e}')
            return jsonify({'error': f'Error deleting the class data: {e}'}), 500

# Main block of code for testing the ClassService
if __name__ == '__main__':
    from models.models import ClassModel
    
    logger = Logger()  # Logger for logging messages
    db_conn = ClassModel()  # Database connection
    class_service = ClassService(db_conn)  # Creating the service with the database connection
    
    try:
        db_conn.connect_to_database()  # Connect to the database
        
        # Fetch all classes and log the result
        classes = class_service.get_all_classes()
        logger.info(f'Classes fetched: {classes}')
        
        # Example operations (currently commented out):
        # Add a new class
        # new_class = class_service.add_class({'role': 'Nahual'})
        # logger.info(f'New class added: {new_class}')
        
        # Get a class by its ID
        # class_data = class_service.get_class_by_id(3)
        # logger.info(f'class: {class_data}')
        
        # Update a class
        # updated_class = class_service.update_class(6, {'author': 'H.P. Lovecraft'})
        # logger.info(f'Updated Class: {updated_class}')
        
        # Delete a class
        # deleted_class = class_service.delete_class(6)
        # logger.info(f'Deleted Class: {deleted_class}')
        
    except Exception as e:
        # If something goes wrong, log the error
        logger.error(f'An error has occurred: {e}')
    finally:
        db_conn.close_connection()  # Close the database connection
        logger.info('Connection to database closed')  # Log that the connection is closed
