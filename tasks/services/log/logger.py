import logging
import os

# Create a logs directory if it doesn't exist
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Define log file paths
INFO_LOG_FILE = os.path.join(LOG_DIR, "info.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")

# Create handlers
info_handler = logging.FileHandler(INFO_LOG_FILE)
info_handler.setLevel(logging.INFO)

error_handler = logging.FileHandler(ERROR_LOG_FILE)
error_handler.setLevel(logging.ERROR)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Define format
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Attach formatters
info_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Get logger
logger = logging.getLogger("project_logger")
logger.setLevel(logging.DEBUG)  # capture everything
logger.addHandler(info_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)
