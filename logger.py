import logging.handlers
import socket

my_logger = logging.getLogger("[Mimas]")
my_logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address=("172.16.16.33", 514), socktype=socket.SOCK_DGRAM)
formatter = logging.Formatter("%(asctime)s; %(name)s %(message)s", datefmt='%Y-%m-%dT%H:%M:%S')
handler.setFormatter(formatter)
my_logger.addHandler(handler)


def insert_log(message, level):
    try:
        if level == "error":
            my_logger.error(message)
        if level == "info":
            my_logger.info(message)
    except Exception as ex:
        return ex
