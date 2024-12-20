from marshmallow import fields, validates, ValidationError

# This npc defines the fields we need to validate
class NpcSchema:
    named = fields.String(required=True)  # Name of the npc, must be a string and is required
    role = fields.String(required=True)  # Npc role, must be a string and required
    picture = fields.String(required=True)  # Picture, must be a string and required
    personality = fields.String(required=True)  # Personality, must be a string and required
    inventory = fields.String(required=True)  # Primary Ability, must be a string and required
    likes = fields.String(required=True)  # Likes, must be a string and required
    money = fields.String(required=True)  # Money, must be a string and required
    backstory = fields.String(required=True)  # Backstory, must be a string and required
    # extra = fields.String(required=False)  # Not using this right now, so it’s commented out

    # Validate the named: Make sure the named has at least 5 characters
    @validates('named')
    def validate_named(self, value):
        if len(value) < 1:
            raise ValidationError('Name must not be empty')

    # Validate the role: Make sure the role has at least 5 characters
    @validates('role')
    def validate_role(self, value):
        if len(value) < 1:
            raise ValidationError('Role must not be empty')
    
    @validates('picture')
    def validate_picture(self, value):
        if len(value) < 5:
            raise ValidationError('Picture URL is too short')
        # Check if the picture is a valid URL
        url_pattern = re.compile(r'^(https?://[^\s/$.?#].[^\s]*|data:[\w+/]+;base64,[^\s]+)$')
        if not url_pattern.match(value):
            raise ValidationError('Picture must be a valid URL.')
            
    # Validate the hit die: Make sure it's at least 2 characters long
    @validates('personality')
    def validate_personality(self, value):
        if len(value) < 1:
            raise ValidationError('Personality must not be empty')

    # Validate the primary ability: Make sure it’s at least 5 characters long
    @validates('inventory')
    def validate_inventory(self, value):
        if len(value) < 1:
            raise ValidationError('Inventory must not be empty')

    # Validate saving throw proficiencies: Make sure it’s at least 5 characters long
    @validates('likes')
    def validate_likes(self, value):
        if len(value) < 1:
            raise ValidationError('Likes must not be empty')

    # Validate armor and weapon proficiencies: Make sure it’s at least 5 characters long
    @validates('money')
    def validate_money(self, value):
        if len(value) < 1:
            raise ValidationError('Money must not be empty')
    
    @validates('backstory')
    def validate_backstory(self, value):
        if len(value) < 1:
            raise ValidationError('Backstory must not be empty')

    # You can also add validation for the "extra" field later if needed
    # @validates('extra')
    # def validate_extra(self, value):
    #     if len(value) > 256:
    #         raise ValidationError('Extra must be at max 256 characters long')

# Main part of the code that runs when the script is executed
if __name__ == '__main__':
    from logger.logger_base import Logger  # Import the custom logger to handle errors
    
    logger = Logger()  # Create a logger instance
    schema = NpcSchema()  # Create a schema instance to validate data
    
    # Example of calling the validation functions:
    # schema.validate_named('Hello')  # Uncomment this to test the named validation
    
    # This try-except block will handle errors if validation fails
    # try:
    #     schema.validate_role('Aut')  # This will fail because it's too short
    # except ValidationError as e:
    #     logger.error(f'An error has occurred: {e}')  # Log the error if something goes wrong
