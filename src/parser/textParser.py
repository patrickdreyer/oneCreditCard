import re
from datetime import datetime
from typing import Iterator

from .transaction import Transaction


class TextParser:
    CATEGORY_PATTERN = re.compile(r"^([^\n*]+?)$", re.MULTILINE)

    # Transaction block pattern - matches the complete transaction structure
    TRANSACTION_PATTERN = re.compile(
        r"(?P<category>^[^\n*]+)\n\n"  # Category on its own line
        r"\*(?P<merchant>[^*]+)\*\n"  # Merchant name in asterisks
        r"(?P<date>\d{2}\.\d{2}\.\d{4})"  # Date DD.MM.YYYY
        r"(?:\s+(?P<time>\d{2}:\d{2}))?"  # Optional time HH:MM
        r"(?:\s+(?P<location>[^\n]+))?\n"  # Optional location
        r"\*(?P<amountChf>-?\d+(?:[\']\d{3})*(?:\.\d{2})?)\*\s+CHF"  # Amount (with optional thousands separator)
        r"(?:\s+(?P<foreignAmount>\d+(?:\.\d{2})?)\s+"  # Foreign amount
        r"(?P<foreignCurrency>EUR|USD))?",  # Foreign currency
        re.MULTILINE,
    )

    def parse(self, text: str) -> Iterator[Transaction]:
        # find all transaction matches
        for match in self.TRANSACTION_PATTERN.finditer(text):
            try:
                transaction = self._parseTransactionMatch(match)
                yield transaction
            except (ValueError, AttributeError) as e:
                # Log error but continue parsing
                print(f"Warning: Failed to parse transaction: {e}")
                continue

    def _parseTransactionMatch(self, match: re.Match) -> Transaction:
        # extract fields
        category = match.group("category").strip()
        merchant = match.group("merchant").strip()
        dateStr = match.group("date")
        timeStr = match.group("time")
        location = match.group("location")
        amountChf = float(match.group("amountChf").replace("'", ""))  # remove thousands separator
        foreignAmountStr = match.group("foreignAmount")
        foreignCurrency = match.group("foreignCurrency")
        date = datetime.strptime(dateStr, "%d.%m.%Y")
        foreignAmount = float(foreignAmountStr) if foreignAmountStr else None

        # clean location
        if location:
            location = location.strip()

        return Transaction(
            category=category,
            merchant=merchant,
            date=date,
            time=timeStr,
            location=location,
            amount=amountChf,
            foreignAmount=foreignAmount,
            foreignCurrency=foreignCurrency,
        )
