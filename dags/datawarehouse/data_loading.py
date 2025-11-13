from datetime import date  
import json
import  logging
import os 

logger = logging.getLogger(__name__)


def load_path():
    """Function to load data from a JSON file and return as a dictionary."""
    """ file_path = f"./data/youtube_data_{date.today()}.json"

    #file_path = f"./data/"
    try:
        logger.info(f"Loading file :youtube_data_{date.today()}.json")
        with open(file_path, "r", encoding= "utf-8") as json_file:
            data = json.load(json_file)
            logger.info(f"Data successfully loaded from {file_path}")
            return data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from file: {file_path}")
        raise
"""
    
    #Load all YouTube JSON files from the ./data/ folder and return a single list of data.
    #Assumes all JSON files are structured as lists or dictionaries.
    folder_path = "./data/"
    all_data = []

    # Filter only files starting with 'youtube_data_' and ending with '.json'
    json_files = [f for f in os.listdir(folder_path) 
                  if f.startswith("youtube_data_") and f.endswith(".json")]

    if not json_files:
        logger.warning(f"No YouTube JSON files found in {folder_path}")
        return all_data

    for file_name in json_files:
        file_path = os.path.join(folder_path, file_name)
        try:
            logger.info(f"Loading file: {file_name}")
            with open(file_path, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
                # If the JSON file is a list, extend the main list; if dict, append
                if isinstance(data, list):
                    all_data.extend(data)
                else:
                    all_data.append(data)
                logger.info(f"Data successfully loaded from {file_path}")
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from file: {file_path}")

    return all_data

