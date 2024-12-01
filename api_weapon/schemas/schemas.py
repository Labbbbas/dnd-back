from marshmallow import fields, validates, ValidationError

# This weapon defines the fields we need to validate
class WeaponSchema:
    named = fields.String(required=True)  # Named of the weapon, must be a string and is required
    category = fields.String(required=True)  # Weapon category, must be a string and required
    cost = fields.String(required=True)  # cost, must be a string and required
    damage = fields.String(required=True)  # Primary Ability, must be a string and required
    properties = fields.String(required=True)  # damage, must be a string and required
    weight = fields.String(required=True)  # weight, must be a string and required
    # extra = fields.String(required=False)  # Not using this right now, so it’s commented out

    # Validate the name: Make sure the name has at least 5 characters
    @validates('named')
    def validate_named(self, value):
        if len(value) < 1:
            raise ValidationError('Weapon name must not be empty')

    # Validate the category: Make sure the category has at least 5 characters
    @validates('category')
    def validate_category(self, value):
        if len(value) < 5:
            raise ValidationError('Description must be at least 5 characters long')

    # Validate the hit die: Make sure it's at least 2 characters long
    @validates('cost')
    def validate_cost(self, value):
        if len(value) < 1:
            raise ValidationError('Cost must not be empty')

    # Validate the primary ability: Make sure it’s at least 5 characters long
    @validates('damage')
    def validate_damage(self, value):
        if len(value) < 1:
            raise ValidationError('Damage must be not be empty')

    # Validate saving throw proficiencies: Make sure it’s at least 5 characters long
    @validates('properties')
    def validate_properties(self, value):
        if len(value) < 1:
            raise ValidationError('Properties must not be empty')

    #Validate the description: Make sure it’s at least 5 characters long
    @validates('description')
    def validate_description(self, value):
        if len(value) < 5:
            raise ValidationError('Description must be at least 5 characters long')

    # Validate armor and weapon proficiencies: Make sure it’s at least 5 characters long
    @validates('weight')
    def validate_weight(self, value):
        if len(value) < 1:
            raise ValidationError('Weight must not be empty')

    # You can also add validation for the "extra" field later if needed
    # @validates('extra')
    # def validate_extra(self, value):
    #     if len(value) > 256:
    #         raise ValidationError('Extra must be at max 256 characters long')

# Main part of the code that runs when the script is executed
if __name__ == '__main__':
    from logger.logger_base import Logger  # Import the custom logger to handle errors
    
    logger = Logger()  # Create a logger instance
    schema = WeaponSchema()  # Create a schema instance to validate data
    
    # Example of calling the validation functions:
    # schema.validate_named('Hello')  # Uncomment this to test the named validation
    
    # This try-except block will handle errors if validation fails
    # try:
    #     schema.validate_category('Aut')  # This will fail because it's too short
    # except ValidationError as e:
    #     logger.error(f'An error has occurred: {e}')  # Log the error if something goes wrong
