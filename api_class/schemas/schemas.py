from marshmallow import fields, validates, ValidationError
import re


# This class defines the fields we need to validate
class ClassSchema:
    role = fields.String(required=True)  # Role of the class, must be a string and is required
    description = fields.String(required=True)  # Class description, must be a string and required
    hd = fields.String(required=True)  # Hit Die (health), must be a string and required
    pa = fields.String(required=True)  # Primary Ability, must be a string and required
    stp = fields.String(required=True)  # Saving Throw Proficiencies, must be a string and required
    awp = fields.String(required=True)  # Armor and Weapon Proficiencies, must be a string and required


    @validates('role')
    def validate_role(self, value):
        # Remove leading and trailing spaces
        value = value.strip()
        
        # Check if the field is empty
        if not value:
            raise ValidationError('Class is required.')
        
        # Check if the value contains only letters (no numbers or special characters)
        if not re.match('^[A-Za-z]+$', value):
            raise ValidationError('Class must contain only letters.')
        

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
        

    @validates('hd')
    def validate_hd(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('Hit Die is required.')
        

    @validates('pa')
    def validate_pa(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('Primary Ability is required.')
        

    @validates('stp')
    def validate_stp(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('Saving Throw Proficiencies is required.')
        
        # Check if the field always contains two elements separated by a comma
        elif value.count(',') != 1:
            raise ValidationError('Saving Throw Proficiencies must always have exactly two selections.')
        

    @validates('awp')
    def validate_awp(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('Armor and Weapon Proficiencies is required.')

        # Check if the length is no more than 200 characters
        elif len(value) > 200:
            raise ValidationError('Armor and Weapon Proficiencies must be no longer than 200 characters.')

        # Check if the value contains only letters, spaces, commas, periods, and parentheses
        if not re.match('^[A-Za-z\\s,.\(\)]+$', value):
            raise ValidationError('Armor and Weapon Proficiencies must contain only letters, spaces, commas, periods, and parentheses.')


# Main part of the code that runs when the script is executed
if __name__ == '__main__':
    from logger.logger_base import Logger  # Import the custom logger to handle errors
    
    logger = Logger()  # Create a logger instance
    schema = ClassSchema()  # Create a schema instance to validate data
    
    # Example of calling the validation functions:
    # schema.validate_role('Hello')  # Uncomment this to test the role validation
    
    # This try-except block will handle errors if validation fails
    # try:
    #     schema.validate_description('Aut')  # This will fail because it's too short
    # except ValidationError as e:
    #     logger.error(f'An error has occurred: {e}')  # Log the error if something goes wrong
