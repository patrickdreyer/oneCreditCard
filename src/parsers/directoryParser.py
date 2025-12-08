from pathlib import Path
from typing import Iterator

from logging_config import getLogger
from .textParser import TextParser
from .transaction import Transaction

logger = getLogger(__name__)


class DirectoryParser:
    def __init__(self):
        self.textParser = TextParser()

    def parse(self, directoryPath: str, filePattern: str = "*.txt") -> Iterator[Transaction]:
        directory = Path(directoryPath)
        if not directory.exists():
            logger.error("Directory not found; path='%s'", directoryPath)
            raise FileNotFoundError(f"Directory not found: {directoryPath}")
        if not directory.is_dir():
            logger.error("Path is not a directory; path='%s'", directoryPath)
            raise ValueError(f"Path is not a directory: {directoryPath}")

        logger.info("Parsing directory; path='%s', pattern='%s'", directoryPath, filePattern)
        fileCount = 0
        transactionCount = 0

        for file in directory.glob(filePattern):
            try:
                fileCount += 1
                fileTransactions = 0
                for transaction in self.__parseFile(str(file)):
                    fileTransactions += 1
                    transactionCount += 1
                    yield transaction
                logger.debug("Parsed file; path='%s', transactions=%d", file, fileTransactions)
            except Exception as e:
                logger.error("Error parsing file; path='%s', error='%s'", file, str(e))
                raise RuntimeError(f"Error parsing file {file}: {e}") from e

        logger.info("Directory parsing complete; files=%d, transactions=%d", fileCount, transactionCount)

    def __parseFile(self, filePath: str) -> Iterator[Transaction]:
        with open(filePath, "r", encoding="utf-8") as file:
            content = file.read()
        yield from self.textParser.parse(content)
