import logging

def get_logger(name, filename, stream=True, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create a file handler
    fh = logging.FileHandler(filename, mode='a', encoding='utf8')
    fh.setLevel(level)

    # Create a stream handler
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    if stream: logger.addHandler(fh)
    logger.addHandler(ch)

    return logger