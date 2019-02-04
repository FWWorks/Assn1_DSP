import logging

loggers = {}

def get_logger(log_file):

    # create logger
    logger_name = log_file
    if logger_name in loggers:
        return loggers[logger_name]
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # create file handler
    log_path = log_file
    fh = logging.FileHandler(log_path, 'w')
    sh = logging.StreamHandler()

    # create formatter
    # fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
    fmt = "%(asctime)-15s %(levelname)s %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)

    # add handler and formatter to logger
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(sh)

    loggers[logger_name] = logger

    return logger