from random import randrange
from socket import AF_INET, SOCK_STREAM, socket


def is_port_in_use(port: int) -> bool:
    with socket(AF_INET, SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def random_port():
    p = randrange(2000, 60000, 100)
    if not is_port_in_use(p):
        yield p
