
import json
from time import time

from app.logger import logger


def save_data_to_file(data, base_filename):
    current_time = str(int(time()))
    filename = "{}_{}.json".format(base_filename, current_time)
    logger.info(f"trying to write: {filename}")
    try:
        with open(filename, "w") as f:
            json.dump(data, f)
    except Exception as exc:
        logger.error(exc)
