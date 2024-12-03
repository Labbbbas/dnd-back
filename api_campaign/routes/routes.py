from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from logger.logger_base import Logger
from flasgger import swag_from

# Define routes for managing campaigns (add, update, delete, etc.)

class CampaignsRoutes(Blueprint):
    def __init__(self, campaign_service, campaign_schema):
        super().__init__('campaign', __name__)  # Initialize the Blueprint
        self.campaign_service = campaign_service  # Service to handle database operations
        self.campaign_schema = campaign_schema  # Schema to validate the campaign data
        self.register_routes()  # Register the routes (endpoints)
        self.logger = Logger()  # Logger for logging messages

    def register_routes(self):
        # Register the HTTP routes for the campaign API
        self.route('/api/v1/campaigns', methods=['GET'])(self.get_campaigns)
        self.route('/api/v1/campaigns', methods=['POST'])(self.add_campaign)
        self.route('/api/v1/campaigns/<int:campaign_id>', methods=['PUT'])(self.update_campaign)
        self.route('/api/v1/campaigns/<int:campaign_id>', methods=['DELETE'])(self.delete_campaign)
        self.route('/healthcheck', methods=['GET'])(self.healthcheck)

    @swag_from({
        'tags': ['Campaigns'],  # API Documentation: Shows this route is for campaigns
        'responses': {
            200: {'description': 'List of campaigns'},
            500: {'description': 'Internal server error'}
        }
    })

    def get_campaigns(self):
        # Get all campaigns from the database
        campaigns = self.campaign_service.get_all_campaigns()
        return jsonify(campaigns), 200  # Return the list of campaigns as JSON

    @swag_from({
        'tags': ['Campaigns'],
        'parameters': [
            {
                'title': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'title': {'type': 'string'},
                        'description': {'type': 'string'},
                        'dm': {'type': 'string'},
                        'status': {'type': 'string'},
                        'pc': {'type': 'string'},
                        'startDate': {'type': 'string'},
                        'endDate': {'type': 'string'},
                        'ql': {'type': 'string'},
                    },
                    'required': ['title', 'description', 'dm', 'status', 'pc', 'startDate', 'endDate','ql']  # These fields are required
                }
            }
        ],
        'responses': {
            201: {'description': 'Campaign successfully created'},
            400: {'description': 'Invalid data'},
            500: {'description': 'Internal server error'}
        }
    })
    def add_campaign(self):
        # Add a new campaign
        try:
            request_data = request.json  # Get the data from the request

            if not request_data:
                return jsonify({'error': 'Invalid data, empty'}), 401  # Check if data is empty

            title = request_data.get('title')
            description = request_data.get('description')
            dm = request_data.get('dm')
            status= request_data.get('status')
            pc = request_data.get('pc')
            startDate = request_data.get('startDate')
            endDate = request_data.get('endDate')
            ql = request_data.get('ql')

            """ # Validate the data using the schema
            try:
                self.campaign_schema.validate_title(title)
                self.campaign_schema.validate_description(description)
                self.campaign_schema.validate_dm(dm)
                self.campaign_schema.validate_sts(status)
                self.campaign_schema.validate_pc(pc)
                self.campaign_schema.validate_startDate(startDate)
                self.campaign_schema.validate_endDate(endDate)
                self.campaign_schema.validate_ql(ql)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data: {e}'}), 402  # Return error if validation fails """

            # Create the new campaign object
            new_campaign = {
                "title": title,
                "description": description,
                "dm": dm,
                "status": status,
                "pc": [
                    {"characterName": char.strip()} for char in (pc if isinstance(pc, list) else pc.split(", "))
                ],
                "startDate": startDate,
                "endDate": endDate,
                "ql": ql,
            }
            created_campaign = self.campaign_service.add_campaign(new_campaign)  # Add the campaign to the database
            self.logger.info(f'New campaign: {created_campaign}')  # Log the new campaign creation
            return jsonify(created_campaign), 201  # Return the created campaign as JSON

        except Exception as e:
            self.logger.error(f'Error adding a new campaign to the database: {e}')
            return jsonify({'error': f'An error has occurred: {e}'}), 500  # Handle any errors

    @swag_from({
        'tags': ['Campaigns'],
        'parameters': [
            {
                'title': 'campaign_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID of the campaign to update'
            },
            {
                'title': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'title': {'type': 'string'},
                        'description': {'type': 'string'},
                        'dm': {'type': 'string'},
                        'status': {'type': 'string'},
                        'pc': {'type': 'string'},
                        'startDate': {'type': 'string'},
                        'endDate': {'type': 'string'},
                        'ql': {'type': 'string'},
                    },
                    'required': ['title', 'description', 'dm', 'status', 'pc', 'startDate', 'endDate', 'ql']  # These fields are required
                }
            }
        ],
        'responses': {
            200: {'description': 'Campaign successfully updated'},
            400: {'description': 'Invalid data'},
            404: {'description': 'Campaign not found'},
            500: {'description': 'Internal server error'}
        }
    })

    def update_campaign(self, campaign_id):
        # Update an existing campaign
        try:
            request_data = request.json  # Get the updated data

            if not request_data:
                return jsonify({'error': 'Invalid data, empty'}), 400  # Check if data is empty

            title = request_data.get('title')
            description = request_data.get('description')
            dm = request_data.get('dm')
            status = request_data.get('status')
            pc = request_data.get('pc')
            startDate = request_data.get('startDate')
            endDate = request_data.get('endDate')
            ql = request_data.get('ql')

            # Validate the data
            try:
                self.campaign_schema.validate_title(title)
            except ValidationError as e:
                self.logger.error(f'Error validating title: {e}')
                return jsonify("Error validating title"), 401  # Return error if validation fails
            try:
                self.campaign_schema.validate_description(description)
            except ValidationError as e:
                self.logger.error(f'Error validating description: {e}')
                return jsonify("Error validating description"), 402
            try:
                self.campaign_schema.validate_dm(dm)
            except ValidationError as e:
                self.logger.error(f'Error validating dm: {e}')
                return jsonify("Error validating dm"), 403
            try:
                self.campaign_schema.validate_sts(status)
            except ValidationError as e:
                self.logger.error(f'Error validating status: {e}')
                return jsonify("Error validating status"), 405
            try:
                self.campaign_schema.validate_pc(pc)
            except ValidationError as e:
                self.logger.error(f'Error validating pc: {e}')
                return jsonify("Error validating pc"), 406
            """ try:
                self.campaign_schema.validate_startDate(startDate)
            except ValidationError as e:
                return jsonify("Error validating start date"), 407 """
            try:
                self.campaign_schema.validate_endDate(endDate)
            except ValidationError as e:
                self.logger.error(f'Error validating end date: {e}')
                return jsonify("Error validating end date"), 408
            
            try:
                self.campaign_schema.validate_ql(ql)
            except ValidationError as e:
                self.logger.error(f'Error validating ql: {e}')
                return jsonify("Error validating ql"), 409

            # Update the campaign object
            update_campaign = {
                '_id': campaign_id,
                'title': title,
                'description': description,
                'dm': dm,
                'status': status,
                'pc': [{'characterName': char.strip()} for char in (pc if isinstance(pc, list) else pc.split(', '))],
                'startDate': startDate,
                'endDate': endDate,
                'ql': ql,
            }

            updated_campaign = self.campaign_service.update_campaign(campaign_id, update_campaign)  # Update the campaign in the database
            if updated_campaign:
                return jsonify(update_campaign), 200  # Return the updated campaign as JSON
            else:
                return jsonify({'error': 'Campaign not found'}), 404  # If campaign not found, return an error

        except Exception as e:
            self.logger.error(f'Error updating the campaign in the database: {e}')
            return jsonify({'error': f'Error updating the campaign in the database: {e}'}), 500  # Handle any errors

    @swag_from({
        'tags': ['Campaigns'],
        'parameters': [
            {
                'title': 'campaign_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID of the campaign to delete'
            }
        ],
        'responses': {
            200: {'description': 'Campaign successfully deleted'},
            404: {'description': 'Campaign not found'},
            500: {'description': 'Internal server error'}
        }
    })
    def delete_campaign(self, campaign_id):
        # Delete a campaign by its ID
        try:
            deleted_campaign = self.campaign_service.delete_campaign(campaign_id)  # Delete the campaign from the database

            if deleted_campaign:
                return jsonify(deleted_campaign), 200  # Return the deleted campaign as JSON
            else:
                return jsonify({'error': 'Campaign not found'}), 404  # If campaign not found, return an error

        except Exception as e:
            self.logger.error(f'Error deleting the campaign from the database: {e}')
            return jsonify({'error': f'Error deleting the campaign from the database: {e}'}), 500  # Handle any errors

    @swag_from({
        'tags': ['Health'],
        'responses': {
            200: {'description': 'Server is up'}
        }
    })
    def healthcheck(self):
        # Health check to verify the server is up
        return jsonify({'status': 'up'}), 200
