from marshmallow import fields, validates, ValidationError

# This boss defines the fields we need to validate
class BossSchema:
    named = fields.String(required=True)  # Name of the boss, must be a string and is required
    typed = fields.String(required=True)  # Boss type, must be a string and required
    picture = fields.String(required=True)  # Picture, must be a string and required
    cr = fields.String(required=True)  # Challenge Rating, must be a string and required
    hp = fields.String(required=True)  # Primary Ability, must be a string and required
    ac = fields.String(required=True)  # Armor Class, must be a string and required
    resistances = fields.String(required=True)  # resistances, must be a string and required
    immunities = fields.String(required=True)  # Immunities, must be a string and required
    abilities = fields.String(required=True)  # Abilities, must be a string and required
    # extra = fields.String(required=False)  # Not using this right now, so it’s commented out

    # Validate the named: Make sure the named has at least 5 characters
    @validates('named')
    def validate_named(self, value):
        if len(value) < 1:
            raise ValidationError('Name must not be empty')

    # Validate the type: Make sure the type has at least 5 characters
    @validates('typed')
    def validate_typed(self, value):
        if len(value) < 1:
            raise ValidationError('Type must not be empty')
    
    @validates('picture')
    def validate_picture(self, value):
        if len(value) < 5:
            raise ValidationError('Picture URL is too short')
        # Check if the picture is a valid URL
        url_pattern = re.compile(r'^(https?://[^\s/$.?#].[^\s]*|data:[\w+/]+;base64,[^\s]+)$')
        if not url_pattern.match(value):
            raise ValidationError('Picture must be a valid URL.')

    # Validate the hit die: Make sure it's at least 2 characters long
    @validates('cr')
    def validate_cr(self, value):
        if len(value) < 1:
            raise ValidationError('Challenge Rating must not be empty')

    # Validate the primary ability: Make sure it’s at least 5 characters long
    @validates('hp')
    def validate_hp(self, value):
        if len(value) < 1:
            raise ValidationError('Hit points must not be empty')

    # Validate saving throw proficiencies: Make sure it’s at least 5 characters long
    @validates('ac')
    def validate_ac(self, value):
        if len(value) < 1:
            raise ValidationError('Armor Class must not be empty')

    # Validate armor and weapon proficiencies: Make sure it’s at least 5 characters long
    @validates('resistances')
    def validate_resistances(self, value):
        if len(value) < 1:
            raise ValidationError('Resistances must not be empty')
    
    @validates('immunities')
    def validate_immunities(self, value):
        if len(value) < 1:
            raise ValidationError('Immunities must not be empty')
    
    @validates('abilities')
    def validate_abilities(self, value):
        if len(value) < 1:
            raise ValidationError('Abilities must not be empty')

    # You can also add validation for the "extra" field later if needed
    # @validates('extra')
    # def validate_extra(self, value):
    #     if len(value) > 256:
    #         raise ValidationError('Extra must be at max 256 characters long')

# Main part of the code that runs when the script is executed
if __name__ == '__main__':
    from logger.logger_base import Logger  # Import the custom logger to handle errors
    
    logger = Logger()  # Create a logger instance
    schema = BossSchema()  # Create a schema instance to validate data
    
    # Example of calling the validation functions:
    # schema.validate_named('Hello')  # Uncomment this to test the named validation
    
    # This try-except block will handle errors if validation fails
    # try:
    #     schema.validate_type('Aut')  # This will fail because it's too short
    # except ValidationError as e:
    #     logger.error(f'An error has occurred: {e}')  # Log the error if something goes wrong
