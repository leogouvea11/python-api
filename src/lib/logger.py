import logging
import sys
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import json
import uuid
from src.middleware.correlation import with_correlation

# Create a custom logger
logger = logging.getLogger("python-api")
logger.setLevel(logging.INFO)

# Create handlers
console_handler = logging.StreamHandler(sys.stdout)
file_handler = RotatingFileHandler(
    "logs/python-api.log",
    maxBytes=1024 * 1024,  # 1MB
    backupCount=5,
    encoding="utf-8",
)

class CustomJsonFormatter(json.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        
        # Always ensure there's a correlation_id, generate one if not present
        log_record['correlation_id'] = getattr(record, 'correlation_id', None)
        
        # Add body if present
        if hasattr(record, 'body'):
            log_record['body'] = record.body

# Update the formatter initialization
log_format = CustomJsonFormatter(
    '%(asctime)s %(name)s %(levelname)s %(message)s %(correlation_id)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
console_handler.setFormatter(log_format)
file_handler.setFormatter(log_format)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Patch logger methods to include correlation ID
logger.info = with_correlation(logger.info)
logger.error = with_correlation(logger.error)
logger.warning = with_correlation(logger.warning)
logger.debug = with_correlation(logger.debug)

# Prevent duplicate logs in case of module reloads
logger.propagate = False 