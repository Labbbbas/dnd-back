from marshmallow import fields, validates, ValidationError
import re

# This schema defines the fields we need to validate for a DND character
class CharacterSchema:
    # Fields with 'required=True' ensure that these attributes must be present
    characterName = fields.String(required=True)  # Character name, must be a non-empty string
    race = fields.String(required=True)  # Race description, must be a non-empty string
    className = fields.String(required=True)  # Class name, must be a non-empty string
    alignment = fields.String(required=True)  # Character alignment, must be a non-empty string
    level = fields.String(required=True)  # Character level, must be a non-empty string
    background = fields.String(required=True)  # Background description, must be a non-empty string
    playerName = fields.String(required=True)  # Player name, must be a non-empty string


    @validates('characterName')
    def validate_characterName(self, value):
        # Remove leading and trailing spaces from the character name
        value = value.strip()
        
        # Check if the character name is empty after stripping spaces
        if not value:
            raise ValidationError('Character name is required.')
        
        # Check if the character name contains any numbers (which are not allowed)
        if any(char.isdigit() for char in value):
            raise ValidationError('Character name cannot contain numbers.')
        
        # Check if the length of the character name is 50 characters or fewer
        if len(value) > 50:
            raise ValidationError('Character name must be 50 characters or fewer.')


    @validates('race')
    def validate_race(self, value):
        # Check if the race description is empty after stripping spaces
        if not value:
            raise ValidationError('Race description is required.')
        
        # Check if the race description contains any numbers (which are not allowed)
        if any(char.isdigit() for char in value):
            raise ValidationError('Race description cannot contain numbers.')
        
        # Check if the length of the race description is 50 characters or fewer
        if len(value) > 50:
            raise ValidationError('Race description must be 50 characters or fewer.')


    @validates('className')
    def validate_className(self, value):
        # Check if the class name is empty after stripping spaces
        if not value:
            raise ValidationError('Class name is required.')
        
        # Check if the class name contains any numbers (which are not allowed)
        if any(char.isdigit() for char in value):
            raise ValidationError('Class name cannot contain numbers.')
        
        # Check if the length of the class name is 50 characters or fewer
        if len(value) > 50:
            raise ValidationError('Class name must be 50 characters or fewer.')


    @validates('alignment')
    def validate_alignment(self, value):
        # Check if the alignment is empty after stripping spaces
        if not value:
            raise ValidationError('Alignment is required.')
        
        
    @validates('level')
    def validate_level(self, value):
        # Check if the level is empty after stripping spaces
        if not value:
            raise ValidationError('Level is required.')
        
        # Ensure the level is a valid number
        if not value.isdigit():
            raise ValidationError('Level must be a number.')
        
        # Convert the value to an integer and check if it is 1 or greater
        if int(value) < 1:
            raise ValidationError('Level must be 1 or higher.')
    
    
    @validates('background')
    def validate_background(self, value):
        # Check if the background description is empty after stripping spaces
        if not value:
            raise ValidationError('Background description is required.')
        
        # Check if the background description contains any numbers (which are not allowed)
        if any(char.isdigit() for char in value):
            raise ValidationError('Background description cannot contain numbers.')
        
        # Check if the length of the background description is 200 characters or fewer
        if len(value) > 200:
            raise ValidationError('Background description must be no longer than 200 characters.')


    @validates('playerName')
    def validate_playerName(self, value):
        # Check if the player name is empty after stripping spaces
        if not value:
            raise ValidationError('Player name is required.')
        
        # Check if the player name contains any numbers (which are not allowed)
        if any(char.isdigit() for char in value):
            raise ValidationError('Player name cannot contain numbers.')
        
        # Check if the length of the player name is 50 characters or fewer
        if len(value) > 50:
            raise ValidationError('Player name must be 50 characters or fewer.')


# Main part of the code that runs when the script is executed
if __name__ == '__main__':
    from logger.logger_base import Logger  # Import the custom logger to handle errors
    
    logger = Logger()  # Create a logger instance
    schema = CharacterSchema()  # Create a schema instance to validate data