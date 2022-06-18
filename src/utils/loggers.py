import logging

class CustomLogger:
    def __init__(self):
        logging.basicConfig(
            format='[%(asctime)s] %(levelname)-8s %(message)s',
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def get_logger(self, name=None):
        return logging.getLogger(name)
    
def get_default_logger():
    return CustomLogger().get_logger()