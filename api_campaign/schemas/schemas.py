from marshmallow import fields, validates, ValidationError
import re


# This campaign defines the fields we need to validate
class CampaignSchema:
    title = fields.String(required=True)  
    description = fields.String(required=True)
    dm = fields.String(required=True)  
    status = fields.String(required=True)
    pc = fields.String(required=True)  
    startDate = fields.String(required=True)  
    endDate = fields.String(required=True)
    ql = fields.String(required=True)  


    @validates('title')
    def validate_title(self, value):
        # Remove leading and trailing spaces
        value = value.strip()
        
        # Check if the field is empty
        if not value:
            raise ValidationError('Campaign is required.')
        
        # Check if the value contains letters. It can also contain numbers, spaces, and common punctuation (, . ' -)
        if not re.match('^[A-Za-z0-9\\s,.\'-]+$', value):
            raise ValidationError('Campaign must contain only letters, numbers, spaces, and common punctuation.')
        
        

    @validates('description')
    def validate_description(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('Description is required.')
        
        # Check if the length is no more than 250 characters
        elif len(value) > 555:
            raise ValidationError('Description must be no longer than 555 characters.')

        # Check if the value contains only letters, spaces, and common punctuation (, . ' -)
        if not re.match('^[A-Za-z\\s,.\'-]+$', value):
            raise ValidationError('Description must contain only letters, spaces, and common punctuation.')
        
    @validates('dm')
    def validate_dm(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('Dungeon Master is required.')
        # Check if the length is no more than 50 characters
        elif len(value) > 50:
            raise ValidationError('Dungeon Master must be no longer than 50 characters.')   

    @validates('status')
    def validate_status(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('Campaign Status is required.')
        # Check if status is different from the options: pending, ongoing, finished
        if value not in ['pending', 'ongoing', 'finished']:
            raise ValidationError('Campaign Status must be one of the following: pending, ongoing, finished.')
        
    @validates('pc')
    def validate_pc(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('At least one Player Character is required.')

    @validates('startDate')
    def validate_startDate(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('Start Date is required.')

        
        
    
    @validates('endDate')
    def validate_endDate(self, value, startDate):
        # Check if the field is empty
        if not value:
            raise ValidationError('End Date is required.')
        # Check if the end date is after the start date
        if value < startDate:
            raise ValidationError('End Date must be after the Start Date.')
    
    @validates('ql')
    def validate_ql(self, value):
        # Check if the length is no more than 500 characters
        if len(value) > 500:
            raise ValidationError('Quest Log must be no longer than 500 characters.')
        # Check if the value contains only letters, spaces, and common punctuation (, . ' -)
        if value and not re.match('^[A-Za-z\\s,.\'-]+$', value):
            raise ValidationError('Quest Log must contain only letters, spaces, and common punctuation.')

# Main part of the code that runs when the script is executed
if __name__ == '__main__':
    from logger.logger_base import Logger  # Import the custom logger to handle errors
    
    logger = Logger()  # Create a logger instance
    schema = CampaignSchema()  # Create a schema instance to validate data
    
    # Example of calling the validation functions:
    # schema.validate_title('Hello')  # Uncomment this to test the title validation
    
    # This try-except block will handle errors if validation fails
    # try:
    #     schema.validate_description('Aut')  # This will fail because it's too short
    # except ValidationError as e:
    #     logger.error(f'An error has occurred: {e}')  # Log the error if something goes wrong
