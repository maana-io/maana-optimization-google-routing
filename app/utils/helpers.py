
import json
from time import time
import logging


def save_data_to_file(data, base_filename):
    current_time = str(int(time()))
    try:
        filename = "{}_{}.json".format(base_filename, current_time)
        logging.info("trying to write: {filename}")
        with open(filename, "w") as f:
            json.dump(data, f)
    except Exception as exc:
        logging.error(exc)
