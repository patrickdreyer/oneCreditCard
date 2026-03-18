from pathlib import Path
from typing import List

from odf.number import DateStyle, Day, Month, Number, NumberStyle, NUMBERNS, Text, Year
from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import Style
from odf.table import Table, TableRow, TableCell
from odf.text import P

from accountMapper import BookingEntry
from configuration import Configuration, ColumnConfig
from logging_config import getLogger

logger = getLogger(__name__)


class OdsGenerator:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration

    def generate(self, entries: List[BookingEntry], outputPath: Path) -> None:
        logger.info("Starting ODS generation; output_path='%s', entries=%d", outputPath, len(entries))

        try:
            doc = OpenDocumentSpreadsheet()
            styleMap = self.__registerStyles(doc)

            table = Table(name="Transactions")
            self.__addHeaderRow(table)

            for idx, entry in enumerate(entries, start=1):
                self.__addDataRow(table, entry, styleMap)
                logger.debug("Row added; row=%d, description='%s', debitAccount='%s'",
                            idx, entry.mappedDescription, entry.debitAccount or "")

            doc.spreadsheet.addElement(table)
            doc.save(str(outputPath))

            logger.info("ODS generation completed; output_path='%s', rows=%d", outputPath, len(entries))
        except Exception as exc:
            logger.error("ODS generation failed; output_path='%s', error='%s'", outputPath, exc)
            raise

    def __registerStyles(self, doc: OpenDocumentSpreadsheet) -> dict:
        styleMap = {}
        for column in self.configuration.columns:
            if column.type != "date":
                continue
            key = f"date:{column.format}"
            if key in styleMap:
                continue
            fmt = column.format
            safeName = fmt.replace(".", "")
            numStyleName = f"dateNum{safeName}"
            cellStyleName = f"dateCell{safeName}"
            ds = DateStyle(name=numStyleName, automaticorder="true")
            ds.addElement(Day(style="long"))
            ds.addElement(Text(text="."))
            ds.addElement(Month(style="long"))
            ds.addElement(Text(text="."))
            ds.addElement(Year(style="long") if fmt == "DD.MM.YYYY" else Year())
            doc.automaticstyles.addElement(ds)
            cs = Style(name=cellStyleName, family="table-cell",
                       parentstylename="Default", datastylename=numStyleName)
            doc.automaticstyles.addElement(cs)
            styleMap[key] = cellStyleName
        if any(col.type == "amountChf" for col in self.configuration.columns):
            ns = NumberStyle(name="amountNum")
            # decimal-places=max, min-decimal-places=min → always exactly 2 places (0.00)
            n = Number(decimalplaces="2", minintegerdigits="1")
            n.attributes[(NUMBERNS, "min-decimal-places")] = "2"
            ns.addElement(n)
            doc.automaticstyles.addElement(ns)
            cs = Style(name="amountCell", family="table-cell",
                       parentstylename="Default", datastylename="amountNum")
            doc.automaticstyles.addElement(cs)
            styleMap["amountChf"] = "amountCell"
        return styleMap

    def __addHeaderRow(self, table: Table) -> None:
        row = TableRow()
        for column in self.configuration.columns:
            cell = TableCell(valuetype="string")
            cell.addElement(P(text=column.name))
            row.addElement(cell)
        table.addElement(row)

    def __addDataRow(self, table: Table, entry: BookingEntry, styleMap: dict) -> None:
        row = TableRow()
        for column in self.configuration.columns:
            row.addElement(self.__createCell(column, entry, styleMap))
        table.addElement(row)

    def __createCell(self, column: ColumnConfig, entry: BookingEntry, styleMap: dict) -> TableCell:
        if column.type == "date":
            return self.__createDateCell(entry, column.format, styleMap.get(f"date:{column.format}"))
        if column.type == "amountChf":
            return self.__createAmountCell(entry, styleMap.get("amountChf"))
        if column.type in ("debitAccount", "creditAccount"):
            return self.__createAccountCell(self.__getCellValue(column, entry))
        value = self.__getCellValue(column, entry)
        if value:
            cell = TableCell(valuetype="string")
            cell.addElement(P(text=value))
            return cell
        return TableCell()

    def __createDateCell(self, entry: BookingEntry, dateFormat: str, cellStyleName: str) -> TableCell:
        date = self.__getDate(entry)
        if date is None:
            return TableCell()
        cell = TableCell(stylename=cellStyleName, valuetype="date", datevalue=date.strftime("%Y-%m-%d"))
        cell.addElement(P(text=self.__formatDateStr(date, dateFormat)))
        return cell

    def __createAccountCell(self, account: str) -> TableCell:
        if not account:
            return TableCell()
        cell = TableCell(valuetype="float", value=account)
        cell.addElement(P(text=account))
        return cell

    def __createAmountCell(self, entry: BookingEntry, cellStyleName: str) -> TableCell:
        amount = self.__getAmount(entry)
        if amount is None:
            return TableCell()
        cell = TableCell(stylename=cellStyleName, valuetype="float", value=f"{amount:.10g}")
        cell.addElement(P(text=f"{amount:.2f}"))
        return cell

    def __getCellValue(self, column: ColumnConfig, entry: BookingEntry) -> str:
        if not column.type:
            # Optional column - check for remarks
            if column.name in ("Bemerkungen", "Bemerkung"):
                return self.__getRemarksValue(entry)
            return ""

        if column.type == "description":
            return entry.mappedDescription
        if column.type == "debitAccount":
            return entry.debitAccount or ""
        if column.type == "creditAccount":
            return entry.creditAccount
        if column.type == "remarks":
            return self.__getRemarksValue(entry)

        return ""

    def __getDate(self, entry: BookingEntry):
        if entry.transaction:
            return entry.transaction.date
        if entry.group:
            return entry.group.monthEndDate
        return None

    def __formatDateStr(self, date, dateFormat: str) -> str:
        if dateFormat == "DD.MM.YY":
            return date.strftime("%d.%m.%y")
        if dateFormat == "DD.MM.YYYY":
            return date.strftime("%d.%m.%Y")
        return date.strftime("%d.%m.%y")

    def __getAmount(self, entry: BookingEntry):
        if entry.transaction:
            return entry.transaction.amount
        if entry.group:
            return entry.group.totalAmount
        return None

    def __getRemarksValue(self, entry: BookingEntry) -> str:
        if entry.transaction and entry.transaction.hasForeignCurrency:
            return f"{entry.transaction.foreignCurrency} {entry.transaction.foreignAmount:.2f}"
        return ""
