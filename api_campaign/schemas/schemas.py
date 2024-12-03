from marshmallow import Schema, fields, validates, ValidationError
import re
from datetime import datetime

# This campaign defines the fields we need to validate
class CampaignSchema (Schema):
    title = fields.String(required=True)         # title of the campaign, must be a string and is required
    description = fields.String(required=True)  # Campaign description, must be a string and required
    dm = fields.String(required=True)           # Dungeon Master, must be a string and required
    status = fields.String(required=True)       # Status, must be a string and required
    # array of player characters, must be their names
    pc = fields.Nested(fields.String(), required=True)  # Player Characters, must be a string and required
    startDate = fields.String(required=True)    # Start Date, must be a string and required
    endDate = fields.String(required=True)      # End Date, must be a string and required
    ql = fields.String(required=True)           # Quest Log, must be a string and is required

    @validates('title')
    def validate_title(self, value):
        # Remove leading and trailing spaces
        value = value.strip()

        # Check if the field is empty
        if not value:
            raise ValidationError('Campaign title is required.')

        # Check if the value contains only letters (no numbers or special characters)
        if not re.match('^[A-Za-z]+$', value):
            raise ValidationError('Campaign title must contain only letters.')

    @validates('description')
    def validate_description(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('Description is required.')

        # Check if the length is no more than 250 characters
        elif len(value) > 250:
            raise ValidationError('Description must be no longer than 250 characters.')

        # Check if the value contains only letters, spaces, and common punctuation (, . ' -)
        if not re.match('^[A-Za-z\\s,.\'-]+$', value):
            raise ValidationError('Description must contain only letters, spaces, and common punctuation.')

    @validates('dm')
    def validate_dm(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('Dungeon Master is required.')

        # Check if the length is no more than 250 characters
        elif len(value) > 200:
            raise ValidationError('Dungeon Master must be no longer than 200 characters.')

        # Check if the value contains only letters, spaces, and common punctuation (, . ' -)
        if not re.match('^[A-Za-z\\s,.\'-]+$', value):
            raise ValidationError('Dungeon Master must contain only letters, spaces, and common punctuation.')

    @validates('status')
    def validate_sts(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('Status is required.')

    @validates('pc')
    def validate_pc(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('Player Characters is required.')

        # Split the value by commas to check how many characters are selected
        # characters = value.split(',')

        # Check if the field always contains two elements separated by a comma
        if len(value) < 2:
            raise ValidationError('Player Characters must always have two or more selections.')

    @validates('startDate')
    def validate_startDate(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('Start Date is required.')

        # Check if the value is a valid date (assuming format MM-DD-YYYY)
        try:
            # Try to parse the value as a date (MM-DD-YYYY)
            start_date = datetime.strptime(value, "%m-%d-%Y")
        except ValueError:
            raise ValidationError('Invalid start date format. Use MM-DD-YYYY.')

    @validates('endDate')
    def validate_endDate(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('End Date is required.')

        # Check if the value is a valid date (assuming format MM-DD-YYYY)
        try:
            # Try to parse the value as a date (MM-DD-YYYY)
            end_date = datetime.strptime(value, '%m-%d-%Y')
        except ValueError:
            raise ValidationError('Invalid end date format. Use MM-DD-YYYY.')

        # Ensure startDate exists (i.e., the campaign has a start date)
        if hasattr(self, 'startDate') and self.startDate:
            # Convert startDate to datetime for comparison
            start_date = datetime.strptime(self.startDate, '%m-%d-%Y')

            # Check if the end date is not before the start date
            if end_date < start_date:  # Direct comparison of startDate and endDate
                raise ValidationError('End Date cannot be earlier than Start Date.')

    @validates('ql')
    def validate_ql(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('Quest Log is required.')

        # Check if the length is no more than 200 characters
        """ elif len(value) > 200:
            raise ValidationError('Quest Log must be no longer than 200 characters.') """

        # Check if the value contains only letters, spaces, commas, periods, and parentheses
        if not re.match('^[A-Za-z\\s,.\(\)]+$', value):
            raise ValidationError('Quest Log must contain only letters, spaces, commas, periods, and parentheses.')

# Main part of the code that runs when the script is executed
if __name__ == '__main__':
    from logger.logger_base import Logger  # Import the custom logger to handle errors
    
    logger = Logger()  # Create a logger instance
    schema = CampaignSchema()  # Create a schema instance to validate data
    
    # Example of calling the validation functions:
    # schema.validate_role('Hello')  # Uncomment this to test the role validation
    
    # This try-except block will handle errors if validation fails
    # try:
    #     schema.validate_description('Aut')  # This will fail because it's too short
    # except ValidationError as e:
    #     logger.error(f'An error has occurred: {e}')  # Log the error if something goes wrong
