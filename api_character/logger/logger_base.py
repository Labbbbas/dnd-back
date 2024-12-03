import logging as log  # Import the logging module

class Logger:
    def __init__(self, log_file='character_api.log', level=log.INFO):
        # Initialize the Logger class with a log file and default log level
        log.basicConfig(
            level=level,  # Set the logging level
            format='%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s',  # Define the log message format
            datefmt='%I:%M:%S %p',  # Set the date and time format for logs
            handlers=[
                log.FileHandler(log_file),  # Write log messages to a file
                log.StreamHandler()  # Display log messages in the console
            ]
        )
        self.logger = log.getLogger()  # Create a logger instance
        
    def debug(self, message):
        # Log a message with DEBUG level
        self.logger.debug(message, stacklevel=2)
    
    def info(self, message):
        # Log a message with INFO level
        self.logger.info(message, stacklevel=2)
    
    def warning(self, message):
        # Log a message with WARNING level
        self.logger.warning(message, stacklevel=2)
        
    def error(self, message):
        # Log a message with ERROR level
        self.logger.error(message, stacklevel=2)
        
    def critical(self, message):
        # Log a message with CRITICAL level
        self.logger.critical(message, stacklevel=2)
        
if __name__ == '__main__':
    # Example usage of the Logger class
    logger = Logger()  # Create a Logger instance
    logger.debug('Message level: DEBUG')  # Log a DEBUG level message
    logger.info('Message level: INFO')  # Log an INFO level message
    logger.warning('Message level: WARNING')  # Log a WARNING level message
    logger.error('Message level: ERROR')  # Log an ERROR level message
    logger.critical('Message level: CRITICAL')  # Log a CRITICAL level message