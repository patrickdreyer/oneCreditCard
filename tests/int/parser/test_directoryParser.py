import pytest

from src.parser import DirectoryParser


class TestDirectoryParser:
    def setup_method(self):
        self.testee = DirectoryParser()  # pylint: disable=attribute-defined-outside-init

    def test_parse_validDirectory_transactions(self, writeFile):
        # arrange
        file1 = writeFile("2025-07_1.txt", """
Essen & Trinken

*Restaurant 1*
31.07.2025 12:00 City1
*10.00*  CHF
<https://one.viseca.ch/de/transaktionen/detail/TRX123>
""")
        writeFile("2025-07_2.txt", """
Shopping

*Shop 1*
31.07.2025 15:00 City2
*20.00*  CHF
<https://one.viseca.ch/de/transaktionen/detail/TRX456>
""")

        # act
        transactions = list(self.testee.parse(str(file1.parent)))

        # assert
        assert len(transactions) == 2
        assert transactions[0].merchant == "Restaurant 1"
        assert transactions[0].amount == 10.00
        assert transactions[1].merchant == "Shop 1"
        assert transactions[1].amount == 20.00

    def test_parse_nonexistentDirectory_error(self):
        # arrange
        nonexistentDir = "/path/to/nonexistent/directory"

        # act & assert
        with pytest.raises(FileNotFoundError, match="Directory not found"):
            list(self.testee.parse(nonexistentDir))

    def test_parse_pathIsFile_error(self, writeFile):
        # arrange
        file = writeFile("test.txt", "content")

        # act & assert
        with pytest.raises(ValueError, match="Path is not a directory"):
            list(self.testee.parse(str(file)))

    def test_parse_noMatchingFiles_emptyResult(self, writeFile):
        # arrange
        csvFile = writeFile("test.csv", "content")

        # act
        transactions = list(self.testee.parse(str(csvFile.parent)))

        # assert
        assert len(transactions) == 0

    def test_parse_customPattern_matchesPattern(self, writeFile):
        # arrange
        datFile = writeFile("data.dat", """
Essen & Trinken

*Test Restaurant*
31.07.2025 12:00 City
*15.00*  CHF
<https://one.viseca.ch/de/transaktionen/detail/TRX123>
""")

        # act
        transactions = list(self.testee.parse(str(datFile.parent), "*.dat"))

        # assert
        assert len(transactions) == 1
        assert transactions[0].amount == 15.00
