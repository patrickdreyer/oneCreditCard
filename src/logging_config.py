import logging
import sys
from pathlib import Path


def setupLogging(logLevel: str = "INFO", logFile: Path = None) -> None:
    # Configure logging with console and optional file output
    level = getattr(logging, logLevel.upper(), logging.INFO)

    # Create formatter with specified pattern
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setLevel(level)
    consoleHandler.setFormatter(formatter)

    # Configure root logger
    rootLogger = logging.getLogger()
    rootLogger.setLevel(level)
    rootLogger.addHandler(consoleHandler)

    # Optional file handler
    if logFile:
        logFile.parent.mkdir(parents=True, exist_ok=True)
        fileHandler = logging.FileHandler(logFile, encoding='utf-8')
        fileHandler.setLevel(level)
        fileHandler.setFormatter(formatter)
        rootLogger.addHandler(fileHandler)


def getLogger(name: str) -> logging.Logger:
    return logging.getLogger(name)
