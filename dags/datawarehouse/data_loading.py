from datetime import date  
import json
import  logging

logger = logging.getLogger(__name__)


def load_path():
    """Function to load data from a JSON file and return as a dictionary."""
    file_path = f"./data/youtube_data_{date.today()}.json"
    try:
        logger.info(f"Loading file :youtube_data_{date.today()}.json")
        with open(file_path, "r", encoding= "utf-8") as json_file:
            data = json.load(json_file)
            logger.info(f"Data successfully loaded from {file_path}")
            return data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from file: {file_path}")
        return {}
