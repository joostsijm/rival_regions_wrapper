"""
Rival Regions Wrapper

This unofficial API wrapper is an implementation
of some Rival Regions functionalities.
"""

import logging
import pathlib2

from appdirs import user_data_dir


DATA_DIR = user_data_dir("rival_regions_wrapper", "bergc")
pathlib2.Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

# get logger
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

# create file handler
FILE_HANDLER = logging.FileHandler("{}/output.log".format(DATA_DIR))
FILE_HANDLER.setLevel(logging.DEBUG)

# create console handler
STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setLevel(logging.INFO)

# create formatter and add it to the handlers
STREAM_FORMATTER = logging.Formatter(
    "%(name)s - %(module)s - %(levelname)s - %(message)s"
)
STREAM_HANDLER.setFormatter(STREAM_FORMATTER)
FILE_FORMATTER = logging.Formatter(
    "%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s"
)
FILE_HANDLER.setFormatter(FILE_FORMATTER)

# add the handlers to logger
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(FILE_HANDLER)

# from .authentication_handler import AuthenticationHandler
# from .middleware import LocalAuthentication, RemoteAuthentication
