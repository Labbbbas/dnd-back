from marshmallow import fields, validates, ValidationError
import re


# This class defines the fields we need to validate
class BossSchema:
    named = fields.String(required=True)  # Name of the Boss, must be a string and is required
    typed = fields.String(required=True)  # Type typed, must be a string and required
    cr = fields.String(required=True)  # CR, must be a string and required
    hp = fields.String(required=True)  # HP, must be a string and required
    ac = fields.String(required=True)  # Saving AC, must be a string and required
    resistances = fields.String(required=True)  # RESISTANCES, must be a string and required
    inmunities = fields.String(required=True)  # INMUNITIES , must be a string and required
    abilities = fields.String(required=True)  # ABILITIES , must be a string and required


    @validates('named')
    def validate_named(self, value):
        # Remove leading and trailing spaces
        value = value.strip()
        
        # Check if the field is empty
        if not value:
            raise ValidationError('Boss is required.')
        
        # Check if the value contains only letters (no numbers or special characters)
        if not re.match('^[A-Za-z]+$', value):
            raise ValidationError('Boss must contain only letters.')
        

    @validates('typed')
    def validate_typed(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('Type is required.')
        
        # Check if the length is no more than 250 characters
        elif len(value) > 50:
            raise ValidationError('Type must be no longer than 50 characters.')

        # Check if the value contains only letters, spaces, and common punctuation (, . ' -)
        if not re.match('^[A-Za-z\s,.\'-]+$', value):
            raise ValidationError('Type must contain only letters, spaces, and common punctuation.')
        

    @validates('cr')
    def validate_cr(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('Challenge Rating is required.')
        

    @validates('hp')
    def validate_hp(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('Hit Points are required.')
        

    @validates('ac')
    def validate_ac(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('Armor Class is required.')
        
        # Check if the field always contains two elements separated by a comma
        elif value.count(',') != 1:
            raise ValidationError('Armor Class must always have exactly two selections.')
        

    @validates('resistances')
    def validate_resistances(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('Resistances are required.')

        # Check if the length is no more than 200 characters
        elif len(value) > 100:
            raise ValidationError('Resistances must be no longer than 100 characters.')

        # Check if the value contains only letters, spaces, commas, periods, and parentheses
        if not re.match('^[A-Za-z\s,.\(\)]+$', value):
            raise ValidationError('Resistances must contain only letters, spaces, commas, periods, and parentheses.')
    
    @validates('inmunities')
    def validate_inmunities(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('Inmunities are required.')

    @validates('abilities')
    def validate_abilities(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('Abilities are required.')

        # Check if the length is no more than 200 characters
        elif len(value) > 100:
            raise ValidationError('Abilities must be no longer than 100 characters.')

        # Check if the value contains only letters, spaces, commas, periods, and parentheses
        if not re.match('^[A-Za-z\s,.\(\)]+$', value):
            raise ValidationError('Abilities must contain only letters, spaces, commas, periods, and parentheses.')

    @validates('picture')
    def validate_picture(self, value):
        # Check if the field is empty
        if not value:
            raise ValidationError('Picture is required.')
        
        # Check if the value contains only letters, numbers, and common punctuation (, . ' -)
        if not re.match('^[A-Za-z0-9\s,.\'-]+$', value):
            raise ValidationError('Picture must contain only letters, numbers, spaces, and common punctuation.')


# Main part of the code that runs when the script is executed
if __name__ == '__main__':
    from logger.logger_base import Logger  # Import the custom logger to handle errors
    
    logger = Logger()  # Create a logger instance
    schema = BossSchema()  # Create a schema instance to validate data
    
    # Example of calling the validation functions:
    # schema.validate_named('Hello')  # Uncomment this to test the named validation
    
    # This try-except block will handle errors if validation fails
    # try:
    #     schema.validate_typed('Aut')  # This will fail because it's too short
    # except ValidationError as e:
    #     logger.error(f'An error has occurred: {e}')  # Log the error if something goes wrong
