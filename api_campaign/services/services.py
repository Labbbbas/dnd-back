# Import necessary modules
from flask import jsonify
from logger.logger_base import Logger

class CampaignService:
    def __init__(self, db_conn):
        # Set up logging and database connection
        self.logger = Logger()  # Logger for logging messages
        self.db_conn = db_conn  # Database connection

    def get_all_campaigns(self):
        try:
            # Fetch all campaigns from the database and return them as a list
            campaigns = list(self.db_conn.db.campaigns.find())
            return campaigns
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error fetching all campaigns from the database: {e}')
            return jsonify({'error': f'Error fetching all campaigns from the database: {e}'}), 500

    def add_campaign(self, new_campaign):
        try:
            # Try to get the highest ID in the collection
            max_campaign = self.db_conn.db.campaigns.find_one(sort=[('_id', -1)])
            # If a campaign exists, increment its ID by 1; otherwise, start from 1
            next_id = max_campaign['_id'] + 1 if max_campaign else 1
            # Assign the new ID to the campaign
            new_campaign['_id'] = next_id  
            # Insert the new campaign into the database
            self.db_conn.db.campaigns.insert_one(new_campaign)
            
            # Return the newly added campaign
            return new_campaign
    
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error creating the new campaign: {e}')
            
            # Return a 500 error response with the error message
            return jsonify({'error': f'Error creating the new campaign: {e}'}), 500

    def get_campaign_by_id(self, campaign_id):
        try:
            # Fetch a specific campaign by its ID from the database
            campaign_data = self.db_conn.db.campaigns.find_one({'_id': campaign_id})
            return campaign_data  # Return the campaign data
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error fetching the campaign id from the database {e}')
            return jsonify({'error': f'Error fetching the campaign id from the database: {e}'}), 500
        
    def update_campaign(self, campaign_id, campaign_data):
        try:
            # First, check if the campaign exists
            update_campaign = self.get_campaign_by_id(campaign_id)

            if update_campaign:
                # If the campaign exists, update it with the new data
                updated_campaign = self.db_conn.db.campaigns.update_one({'_id': campaign_id}, {'$set': campaign_data})
                if updated_campaign.modified_count > 0:
                    return updated_campaign  # Return the updated campaign
                else:
                    return 'The campaign is already up-to-date'  # No changes made
            else:
                return None  # Campaign not found
            
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error updating the campaign: {e}')
            return jsonify({'error': f'Error updating the campaign: {e}'}), 500
        
    def delete_campaign(self, campaign_id):
        try:
            # Check if the campaign exists before deleting
            deleted_campaign = self.get_campaign_by_id(campaign_id)
            
            if deleted_campaign:
                # If the campaign exists, delete it from the database
                self.db_conn.db.campaigns.delete_one({'_id': campaign_id})
                return deleted_campaign  # Return the deleted campaign data
            else:
                return None  # Campaign not found
            
        except Exception as e:
            # If something goes wrong, log the error and return an error message
            self.logger.error(f'Error deleting the campaign data: {e}')
            return jsonify({'error': f'Error deleting the campaign data: {e}'}), 500

# Main block of code for testing the CampaignService
if __name__ == '__main__':
    from models.models import CampaignModel
    
    logger = Logger()  # Logger for logging messages
    db_conn = CampaignModel()  # Database connection
    campaign_service = CampaignService(db_conn)  # Creating the service with the database connection
    
    try:
        db_conn.connect_to_database()  # Connect to the database
        
        # Fetch all campaigns and log the result
        campaigns = campaign_service.get_all_campaigns()
        logger.info(f'Campaigns fetched: {campaigns}')
        
        # Example operations (currently commented out):
        # Add a new campaign
        # new_campaign = campaign_service.add_campaign({'role': 'Nahual'})
        # logger.info(f'New campaign added: {new_campaign}')
        
        # Get a campaign by its ID
        # campaign_data = campaign_service.get_campaign_by_id(3)
        # logger.info(f'campaign: {campaign_data}')
        
        # Update a campaign
        # updated_campaign = campaign_service.update_campaign(6, {'author': 'H.P. Lovecraft'})
        # logger.info(f'Updated Campaign: {updated_campaign}')
        
        # Delete a campaign
        # deleted_campaign = campaign_service.delete_campaign(6)
        # logger.info(f'Deleted Campaign: {deleted_campaign}')
        
    except Exception as e:
        # If something goes wrong, log the error
        logger.error(f'An error has occurred: {e}')
    finally:
        db_conn.close_connection()  # Close the database connection
        logger.info('Connection to database closed')  # Log that the connection is closed
