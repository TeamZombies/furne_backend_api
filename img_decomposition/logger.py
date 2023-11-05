import logging

# Define a function to configure and return a logger
# Note: call with __name__ to use the name of the calling module
# Note: valid log levels are: DEBUG, INFO, WARNING, ERROR, CRITICAL
def get_logger(name, level=logging.INFO) -> logging.Logger: 
    # Create a logger with the given name
    logger = logging.getLogger(name=name)
    
    # Create a StreamHandler object that writes log messages to the console
    handler = logging.StreamHandler()
    
    # Configure the handler to use a specific log message format
    # E.g., INFO: 2021-01-01 00:00:00,000, api - This is a log message.
    handler.setFormatter(
        fmt=logging.Formatter(fmt="%(levelname)s: %(asctime)s, %(name)s - %(message)s")
    )
    
    # Add the configured handler to the logger
    logger.addHandler(hdlr=handler)
    # Set the logger to filter messages at or above the specified level
    logger.setLevel(level=level)
    # Prevent log messages from propagating to the handlers of ancestor loggers
    logger.propagate = False
    
     # Return the configured logger
    return logger
