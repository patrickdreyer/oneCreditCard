from datetime import datetime
import pytest

from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P

from odsGenerator import OdsGenerator
from accountMapper import BookingEntry
from configuration import Configuration
from parsers.transaction import Transaction
from transactionGrouper import Group


class TestOdsGenerator:
    @pytest.fixture(autouse=True)
    def setup(self, writeConfig, tmp_path):
        configData = {
            "creditAccount": "2110",
            "mapping": {},
            "columns": [
                {"name": "Datum", "type": "date", "format": "DD.MM.YY"},
                {"name": "Beschreibung", "type": "description"},
                {"name": "KtSoll", "type": "debitAccount"},
                {"name": "KtHaben", "type": "creditAccount"},
                {"name": "Betrag CHF", "type": "amountChf"},
                {"name": "Bemerkungen", "type": "remarks"}
            ]
        }
        config = Configuration(writeConfig(configData))
        self.testee = OdsGenerator(config)  # pylint: disable=attribute-defined-outside-init
        self.outputDir = tmp_path  # pylint: disable=attribute-defined-outside-init

    def test_generate_singleTransaction_odsFile(self):
        # arrange
        transaction = Transaction("Food", "Restaurant", datetime(2025, 7, 15), "12:30", "Zurich", 25.50)
        entries = [BookingEntry("Verpflegung", "5821", "2110", transaction=transaction)]
        outputPath = self.outputDir / "test.ods"

        # act
        self.testee.generate(entries, outputPath)

        # assert
        assert outputPath.exists()
        doc = load(str(outputPath))
        tables = doc.spreadsheet.getElementsByType(Table)
        assert len(tables) == 1

        rows = tables[0].getElementsByType(TableRow)
        assert len(rows) == 2  # Header + 1 data row

    def test_generate_singleTransaction_correctData(self):
        # arrange
        transaction = Transaction("Food", "Restaurant", datetime(2025, 7, 15), "12:30", "Zurich", 25.50)
        entries = [BookingEntry("Verpflegung", "5821", "2110", transaction=transaction)]
        outputPath = self.outputDir / "test.ods"

        # act
        self.testee.generate(entries, outputPath)

        # assert
        doc = load(str(outputPath))
        tables = doc.spreadsheet.getElementsByType(Table)
        rows = tables[0].getElementsByType(TableRow)

        # Check data row
        dataRow = rows[1]
        cells = dataRow.getElementsByType(TableCell)
        assert len(cells) == 6

        # Extract cell values
        values = [self.__getCellText(cell) for cell in cells]
        assert values[0] == "15.07.25"  # Date
        assert values[1] == "Verpflegung"  # Description
        assert values[2] == "5821"  # Debit account
        assert values[3] == "2110"  # Credit account
        assert values[4] == "25.50"  # Amount
        assert values[5] == ""  # Remarks (no foreign currency)

    def test_generate_transactionWithForeignCurrency_remarksColumn(self):
        # arrange
        transaction = Transaction("Shopping", "Amazon", datetime(2025, 7, 20), None, None, 285.05, 297.00, "EUR")
        entries = [BookingEntry("Online Shopping", "5811", "2110", transaction=transaction)]
        outputPath = self.outputDir / "test.ods"

        # act
        self.testee.generate(entries, outputPath)

        # assert
        doc = load(str(outputPath))
        tables = doc.spreadsheet.getElementsByType(Table)
        rows = tables[0].getElementsByType(TableRow)
        dataRow = rows[1]
        cells = dataRow.getElementsByType(TableCell)
        values = [self.__getCellText(cell) for cell in cells]

        assert values[5] == "EUR 297.00"  # Remarks with foreign currency

    def test_generate_groupedTransactions_monthEndDate(self):
        # arrange
        group = Group("Food", 100.50, 3, datetime(2025, 7, 31), [])
        entries = [BookingEntry("Verpflegung", "5821", "2110", group=group)]
        outputPath = self.outputDir / "test.ods"

        # act
        self.testee.generate(entries, outputPath)

        # assert
        doc = load(str(outputPath))
        tables = doc.spreadsheet.getElementsByType(Table)
        rows = tables[0].getElementsByType(TableRow)
        dataRow = rows[1]
        cells = dataRow.getElementsByType(TableCell)
        values = [self.__getCellText(cell) for cell in cells]

        assert values[0] == "31.07.25"  # Month end date
        assert values[4] == "100.50"  # Total amount

    def test_generate_unmappedTransaction_emptyDebitAccount(self):
        # arrange
        transaction = Transaction("Unknown", "Store", datetime(2025, 7, 15), None, None, 50.00)
        entries = [BookingEntry("Store", None, "2110", transaction=transaction)]
        outputPath = self.outputDir / "test.ods"

        # act
        self.testee.generate(entries, outputPath)

        # assert
        doc = load(str(outputPath))
        tables = doc.spreadsheet.getElementsByType(Table)
        rows = tables[0].getElementsByType(TableRow)
        dataRow = rows[1]
        cells = dataRow.getElementsByType(TableCell)
        values = [self.__getCellText(cell) for cell in cells]

        assert values[2] == ""  # Empty debit account

    def test_generate_multipleEntries_multipleRows(self):
        # arrange
        t1 = Transaction("Food", "Restaurant", datetime(2025, 7, 15), None, None, 25.50)
        t2 = Transaction("Transport", "SBB", datetime(2025, 7, 16), None, None, 15.00)
        entries = [
            BookingEntry("Verpflegung", "5821", "2110", transaction=t1),
            BookingEntry("Verkehr", "6282", "2110", transaction=t2)
        ]
        outputPath = self.outputDir / "test.ods"

        # act
        self.testee.generate(entries, outputPath)

        # assert
        doc = load(str(outputPath))
        tables = doc.spreadsheet.getElementsByType(Table)
        rows = tables[0].getElementsByType(TableRow)
        assert len(rows) == 3  # Header + 2 data rows

    def test_generate_withOptionalColumns_emptyValues(self, writeConfig):
        # arrange
        configData = {
            "creditAccount": "2110",
            "mapping": {},
            "columns": [
                {"name": "Datum", "type": "date", "format": "DD.MM.YY"},
                {"name": "Beschreibung", "type": "description"},
                {"name": "Saldo"},  # Optional column
                {"name": "KS1"}  # Optional column
            ]
        }
        config = Configuration(writeConfig(configData))
        testee = OdsGenerator(config)

        transaction = Transaction("Food", "Restaurant", datetime(2025, 7, 15), None, None, 25.50)
        entries = [BookingEntry("Verpflegung", "5821", "2110", transaction=transaction)]
        outputPath = self.outputDir / "optional.ods"

        # act
        testee.generate(entries, outputPath)

        # assert
        doc = load(str(outputPath))
        tables = doc.spreadsheet.getElementsByType(Table)
        rows = tables[0].getElementsByType(TableRow)
        dataRow = rows[1]
        cells = dataRow.getElementsByType(TableCell)
        values = [self.__getCellText(cell) for cell in cells]

        assert values[2] == ""  # Optional Saldo column
        assert values[3] == ""  # Optional KS1 column

    def __getCellText(self, cell: TableCell) -> str:
        paragraphs = cell.getElementsByType(P)
        if paragraphs:
            return str(paragraphs[0])
        return ""
