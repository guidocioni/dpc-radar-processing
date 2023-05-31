import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(processName)s %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
