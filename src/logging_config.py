import logging
import sys
from pathlib import Path


LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_FORMAT = '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'


class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG':    '\033[36m', # cyan
        'INFO':     '\033[32m', # green
        'WARNING':  '\033[33m', # yellow
        'ERROR':    '\033[31m', # red
        'CRITICAL': '\033[41m', # red background
    }
    RESET = '\033[0m'

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname:<8}{self.RESET}"
        return super().format(record)


def setupLogging(logLevel: str = "INFO", logFile: Path = Path('onecreditcard.log')) -> None:
    # Configure logging with console and optional file output
    level = getattr(logging, logLevel.upper(), logging.INFO)

    # Console handler
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(ColorFormatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT))

    # Configure root logger
    rootLogger = logging.getLogger()
    rootLogger.setLevel(level)
    rootLogger.addHandler(consoleHandler)

    # Optional file handler
    if logFile:
        logFile.parent.mkdir(parents=True, exist_ok=True)
        fileHandler = logging.FileHandler(logFile, encoding='utf-8')
        fileHandler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT))
        rootLogger.addHandler(fileHandler)


def getLogger(name: str) -> logging.Logger:
    return logging.getLogger(name)
