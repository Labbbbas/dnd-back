from marshmallow import fields, validates, ValidationError

# This class defines the fields we need to validate
class ClassSchema:
    role = fields.String(required=True)  # Role of the class, must be a string and is required
    description = fields.String(required=True)  # Class description, must be a string and required
    hd = fields.String(required=True)  # Hit Die (health), must be a string and required
    pa = fields.String(required=True)  # Primary Ability, must be a string and required
    stp = fields.String(required=True)  # Saving Throw Proficiencies, must be a string and required
    awp = fields.String(required=True)  # Armor and Weapon Proficiencies, must be a string and required
    # extra = fields.String(required=False)  # Not using this right now, so it’s commented out

    # Validate the role: Make sure the role has at least 5 characters
    @validates('role')
    def validate_role(self, value):
        if len(value) < 5:
            raise ValidationError('Class must be at least 5 characters long')

    # Validate the description: Make sure the description has at least 5 characters
    @validates('description')
    def validate_description(self, value):
        if len(value) < 5:
            raise ValidationError('Description must be at least 5 characters long')

    # Validate the hit die: Make sure it's at least 2 characters long
    @validates('hd')
    def validate_hd(self, value):
        if len(value) < 2:
            raise ValidationError('Hit Die must be at least 2 characters long')

    # Validate the primary ability: Make sure it’s at least 5 characters long
    @validates('pa')
    def validate_pa(self, value):
        if len(value) < 5:
            raise ValidationError('Primary Ability must be at least 5 characters long')

    # Validate saving throw proficiencies: Make sure it’s at least 5 characters long
    @validates('stp')
    def validate_stp(self, value):
        if len(value) < 5:
            raise ValidationError('Saving Throw Proficiencies must be at least 5 characters long')

    # Validate armor and weapon proficiencies: Make sure it’s at least 5 characters long
    @validates('awp')
    def validate_awp(self, value):
        if len(value) < 5:
            raise ValidationError('Armor and Weapon Proficiencies must be at least 5 characters long')

    # You can also add validation for the "extra" field later if needed
    # @validates('extra')
    # def validate_extra(self, value):
    #     if len(value) > 256:
    #         raise ValidationError('Extra must be at max 256 characters long')

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
