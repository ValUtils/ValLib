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


class LogEnv:
    level: int
    console: bool
    file: bool
    path: Path

    @classmethod
    def env(cls, logger: logging.Logger):
        logenv = cls()
        logenv.level = int_env(logger, "LOG_LEVEL", Level.INFO)
        logenv.console = bool_env(logger, "LOG_CONSOLE", True)
        logenv.file = bool_env(logger, "LOG_FILE_ENABLE", False)
        logenv.path = Path(get_env(logger, "LOG_FILE", ""))
        return logenv


def get_env(logger: logging.Logger, key: str, default):
    return getenv(f"{logger.name}_{key}", default)


def bool_env(logger: logging.Logger, key: str, default: bool):
    return bool(int(get_env(logger, key, default)))


def int_env(logger: logging.Logger, key: str, default: int):
    return int(get_env(logger, key, default))


def add_levels():
    for l in Level:
        logging.addLevelName(l, l.name)


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


def general():
    l = LogEnv()
    l.level = int(getenv("VALUTILS_LEVEL", Level.INFO))
    l.console = bool(int(getenv("VALUTILS_CONSOLE", False)))
    l.file = bool(int(getenv("VALUTILS_FILE_ENABLE", False)))
    l.path = Path(getenv("VALUTILS_FILE", ""))
    return l


def env_setup(logger: logging.Logger):
    l = LogEnv.env(logger)
    gen = general()
    logger.setLevel(min(l.level, gen.level))
    if l.console or gen.console:
        stderr(logger)
    if l.file:
        file_out(logger, l.path)
    if gen.file:
        file_out(logger, gen.path)


add_levels()

logger = logging.getLogger(LOGGER_NAME)

env_setup(logger)


def log(level: int, msg: object, child=None):
    if child is not None:
        logger.getChild(child).log(level, msg)
        return
    logger.log(level, msg)


__all__ = ["Level", "log"]
