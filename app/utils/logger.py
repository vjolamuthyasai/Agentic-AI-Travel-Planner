import logging
import os

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("travel_planner.log")
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logger()