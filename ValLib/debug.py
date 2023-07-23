import logging
from enum import IntEnum
from os import getenv
from pathlib import Path

LOGGER_NAME = "ValLib"


class Level(IntEnum):
    INFO = logging.INFO
    EXTRA = 15
    DEBUG = logging.DEBUG
    FULL = 5
    VERBOSE = 1


def get_env(logger: logging.Logger, key: str, default):
    return getenv(f"{logger.name}_{key}", default)


def add_levels():
    for l in Level:
        logging.addLevelName(l, str(l).split(".")[1])


def stderr(logger: logging.Logger):
    fmt = logging.Formatter('%(name)s:%(levelname)s -> %(message)s')
    h = logging.StreamHandler()
    h.setFormatter(fmt)
    logger.addHandler(h)


def file_out(logger: logging.Logger, path: Path):
    fmt = logging.Formatter(
        '%(asctime)s %(name)s:%(levelname)s -> %(message)s')
    h = logging.FileHandler(path)
    h.setFormatter(fmt)
    logger.addHandler(h)


def env_setup(logger: logging.Logger):
    level = int(get_env(logger, "LOG_LEVEL", Level.INFO))
    logger.setLevel(level)
    console = bool(int(get_env(logger, "LOG_CONSOLE", True)))
    if console:
        stderr(logger)
    file = bool(int(get_env(logger, "LOG_FILE_ENABLE", False)))
    file_path = Path(get_env(logger, "LOG_FILE", ""))
    if file:
        file_out(logger, file_path)


add_levels()

logger = logging.getLogger(LOGGER_NAME)

env_setup(logger)


def log(level: int, msg: object, child=None):
    if child is not None:
        logger.getChild(child).log(level, msg)
        return
    logger.log(level, msg)


__all__ = ["Level", "log"]
