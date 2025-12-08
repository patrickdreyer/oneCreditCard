from datetime import datetime

from parsers import TextParser


class TestTextParser:
    def setup_method(self):
        self.testee = TextParser()  # pylint: disable=attribute-defined-outside-init

    def test_parse_simple_transaction(self):
        # arrange
        text = """
Essen & Trinken

*- My Lunch Place*
31.07.2025 13:14 Olten
*4.30*  CHF
<https://one.viseca.ch/de/transaktionen/detail/TRX123245678>
"""
        # act
        transactions = list(self.testee.parse(text))

        # assert
        assert len(transactions) == 1
        trans = transactions[0]
        assert trans.category == "Essen & Trinken"
        assert trans.merchant == "- My Lunch Place"
        assert trans.date == datetime(2025, 7, 31)
        assert trans.time == "13:14"
        assert trans.location == "Olten"
        assert trans.amount == 4.30
        assert trans.foreignAmount is None
        assert trans.foreignCurrency is None

    def test_parse_entryWithForeignCurrency_transactionWithForeignCurrency(self):
        # arrange
        text = """
Shopping

*shop.company.com*
22.07.2025 20:07
*285.05*  CHF 297.00  EUR
<https://one.viseca.ch/de/transaktionen/detail/TRX123245678>
"""
        # act
        transactions = list(self.testee.parse(text))

        # assert
        assert len(transactions) == 1
        trans = transactions[0]
        assert trans.category == "Shopping"
        assert trans.merchant == "shop.company.com"
        assert trans.date == datetime(2025, 7, 22)
        assert trans.time == "20:07"
        assert trans.location is None
        assert trans.amount == 285.05
        assert trans.foreignAmount == 297.00
        assert trans.foreignCurrency == "EUR"

    def test_parse_entryWithoutTimeAndLocation_transactionWithoutTimeAndLocation(self):
        # arrange
        text = """
TRX123245678

*SBB CFF FFS*
24.07.2025
*6.40*  CHF
<https://one.viseca.ch/de/transaktionen/detail/TRX123245678>
"""
        # act
        transactions = list(self.testee.parse(text))

        # assert
        assert len(transactions) == 1
        trans = transactions[0]
        assert trans.category == "TRX123245678"
        assert trans.merchant == "SBB CFF FFS"
        assert trans.date == datetime(2025, 7, 24)
        assert trans.time is None
        assert trans.location is None
        assert trans.amount == 6.40

    def test_parse_Payments_negativeAmount(self):
        # arrange
        text = """
Einlagen

*Ihre Zahlung - Danke*
22.07.2025
*-157.95*  CHF
<https://one.viseca.ch/de/transaktionen/detail/TRX123245678>
"""
        # act
        transactions = list(self.testee.parse(text))

        # assert
        assert len(transactions) == 1
        trans = transactions[0]
        assert trans.category == "Einlagen"
        assert trans.merchant == "Ihre Zahlung - Danke"
        assert trans.amount == -157.95

    def test_parse_threeEntries_threeTransactions(self):
        # arrange
        text = """
Essen & Trinken

*Restaurant 1*
28.07.2025 19:19 Zug
*18.50*  CHF
<https://one.viseca.ch/de/transaktionen/detail/TRX123245678>

Essen & Trinken

*Cafe 1*
28.07.2025 17:38 Zurich
*10.00*  CHF
<https://one.viseca.ch/de/transaktionen/detail/TRX123245678>

Fahrzeug

*Gasstation 1*
31.07.2025 15:34 Winterthur
*85.25*  CHF
<https://one.viseca.ch/de/transaktionen/detail/TRX123245678>
"""
        # act
        transactions = list(self.testee.parse(text))

        # assert
        assert len(transactions) == 3

        # Check first transaction
        assert transactions[0].category == "Essen & Trinken"
        assert transactions[0].merchant == "Restaurant 1"
        assert transactions[0].amount == 18.50

        # Check second transaction
        assert transactions[1].category == "Essen & Trinken"
        assert transactions[1].merchant == "Cafe 1"
        assert transactions[1].amount == 10.00

        # Check third transaction
        assert transactions[2].category == "Fahrzeug"
        assert transactions[2].merchant == "Gasstation 1"
        assert transactions[2].amount == 85.25

    def test_parse_emptyEntry_noTransactions(self):
        # act
        transactions = list(self.testee.parse(""))

        # assert
        assert len(transactions) == 0

    def test_parse_invalidEntry_noTransactions(self):
        # arrange
        text = """
This is just some random text
without any transaction data
"""
        # act
        transactions = list(self.testee.parse(text))

        # assert
        assert len(transactions) == 0

    def test_parse_merchantWithExtraWhitespace_transactionWithTrimmedMerchant(self):
        # arrange
        text = """
Essen & Trinken

*  Restaurant with spaces  *
31.07.2025 12:00 City
*25.50*  CHF
<https://one.viseca.ch/de/transaktionen/detail/TRX123245678>
"""
        # act
        transactions = list(self.testee.parse(text))

        # assert
        assert len(transactions) == 1
        assert transactions[0].merchant == "Restaurant with spaces"
