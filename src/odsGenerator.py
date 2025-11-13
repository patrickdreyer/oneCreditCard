from pathlib import Path
from typing import List

from odf.opendocument import OpenDocumentSpreadsheet
from odf.table import Table, TableRow, TableCell
from odf.text import P

from src.accountMapper import BookingEntry
from src.configuration import Configuration, ColumnConfig


class OdsGenerator:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration

    def generate(self, entries: List[BookingEntry], outputPath: Path) -> None:
        doc = OpenDocumentSpreadsheet()

        table = Table(name="Transactions")
        self.__addHeaderRow(table)

        for entry in entries:
            self.__addDataRow(table, entry)

        doc.spreadsheet.addElement(table)
        doc.save(str(outputPath))

    def __addHeaderRow(self, table: Table) -> None:
        row = TableRow()
        for column in self.configuration.columns:
            cell = TableCell()
            cell.addElement(P(text=column.name))
            row.addElement(cell)
        table.addElement(row)

    def __addDataRow(self, table: Table, entry: BookingEntry) -> None:
        row = TableRow()

        for column in self.configuration.columns:
            cell = TableCell()
            value = self.__getCellValue(column, entry)
            if value:
                cell.addElement(P(text=str(value)))
            row.addElement(cell)

        table.addElement(row)

    def __getCellValue(self, column: ColumnConfig, entry: BookingEntry) -> str:
        if not column.type:
            # Optional column - check for remarks
            if column.name == "Bemerkungen" or column.name == "Bemerkung":
                return self.__getRemarksValue(entry)
            return ""

        if column.type == "date":
            return self.__formatDate(entry, column.format)
        elif column.type == "description":
            return entry.mappedDescription
        elif column.type == "debitAccount":
            return entry.debitAccount or ""
        elif column.type == "creditAccount":
            return entry.creditAccount
        elif column.type == "amountChf":
            return self.__formatAmount(entry)
        elif column.type == "remarks":
            return self.__getRemarksValue(entry)

        return ""

    def __formatDate(self, entry: BookingEntry, dateFormat: str) -> str:
        if entry.transaction:
            date = entry.transaction.date
        elif entry.group:
            date = entry.group.monthEndDate
        else:
            return ""

        # Convert DD.MM.YY format to Python strftime format
        if dateFormat == "DD.MM.YY":
            return date.strftime("%d.%m.%y")
        elif dateFormat == "DD.MM.YYYY":
            return date.strftime("%d.%m.%Y")
        else:
            return date.strftime("%d.%m.%y")

    def __formatAmount(self, entry: BookingEntry) -> str:
        if entry.transaction:
            amount = entry.transaction.amount
        elif entry.group:
            amount = entry.group.totalAmount
        else:
            return ""

        return f"{amount:.2f}"

    def __getRemarksValue(self, entry: BookingEntry) -> str:
        if entry.transaction and entry.transaction.hasForeignCurrency:
            return f"{entry.transaction.foreignCurrency} {entry.transaction.foreignAmount:.2f}"
        return ""
