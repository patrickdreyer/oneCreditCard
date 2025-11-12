from pathlib import Path
from typing import Iterator

from .textParser import TextParser
from .transaction import Transaction


class DirectoryParser:
    def __init__(self):
        self.textParser = TextParser()

    def parse(self, directoryPath: str, filePattern: str = "*.txt") -> Iterator[Transaction]:
        directory = Path(directoryPath)
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directoryPath}")
        if not directory.is_dir():
            raise ValueError(f"Path is not a directory: {directoryPath}")

        for file in directory.glob(filePattern):
            try:
                yield from self.__parseFile(str(file))
            except Exception as e:
                raise RuntimeError(f"Error parsing file {file}: {e}") from e

    def __parseFile(self, filePath: str) -> Iterator[Transaction]:
        with open(filePath, "r", encoding="utf-8") as file:
            content = file.read()
        yield from self.textParser.parse(content)
