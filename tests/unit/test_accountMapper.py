from datetime import datetime
import pytest

from src.accountMapper import AccountMapper
from src.configuration import Configuration
from src.parser.transaction import Transaction
from src.transactionGrouper import Group


class TestAccountMapper:
    @pytest.fixture(autouse=True)
    def setup(self, writeConfig):
        configData = {
            "creditAccount": "2110",
            "ignore": {
                "categories": ["Einlagen"],
                "transactions": ["PAYMENT.*"]
            },
            "mapping": {
                "Essen & Trinken": {
                    "description": "Verpflegung",
                    "debitAccount": "5821"
                },
                "Transport": {
                    "pattern": "^SBB.*",
                    "description": "Öffentlicher Verkehr",
                    "debitAccount": "6282"
                }
            },
            "columns": []
        }
        config = Configuration(writeConfig("test.json", configData))
        self.testee = AccountMapper(config)  # pylint: disable=attribute-defined-outside-init

    def test_mapTransactions_mappedCategory_bookingEntry(self):
        # arrange
        transactions = [Transaction(
            "Essen & Trinken", "Restaurant", datetime(2025, 7, 15), None, None, 25.50)]

        # act
        result = list(self.testee.mapTransactions(transactions))

        # assert
        assert len(result) == 1
        entry = result[0]
        assert entry.mappedDescription == "Verpflegung"
        assert entry.debitAccount == "5821"
        assert entry.creditAccount == "2110"
        assert entry.transaction == transactions[0]
        assert entry.group is None

    def test_mapTransactions_unmappedCategory_bookingEntryWithoutDebit(self):
        # arrange
        transactions = [Transaction(
            "Unknown", "Some Store", datetime(2025, 7, 15), None, None, 50.00)]

        # act
        result = list(self.testee.mapTransactions(transactions))

        # assert
        assert len(result) == 1
        entry = result[0]
        assert entry.mappedDescription == "Some Store"
        assert entry.debitAccount is None
        assert entry.creditAccount == "2110"
        assert entry.transaction == transactions[0]

    def test_mapTransactions_patternMatch_bookingEntry(self):
        # arrange
        transactions = [
            Transaction("Transport", "SBB CFF FFS", datetime(
                2025, 7, 15), None, None, 15.00)
        ]

        # act
        result = list(self.testee.mapTransactions(transactions))

        # assert
        assert len(result) == 1
        entry = result[0]
        assert entry.mappedDescription == "Öffentlicher Verkehr"
        assert entry.debitAccount == "6282"

    def test_mapTransactions_patternNoMatch_bookingEntryWithoutDebit(self):
        # arrange
        transactions = [
            Transaction("Transport", "Taxi", datetime(
                2025, 7, 15), None, None, 30.00)
        ]

        # act
        result = list(self.testee.mapTransactions(transactions))

        # assert
        assert len(result) == 1
        entry = result[0]
        assert entry.mappedDescription == "Taxi"
        assert entry.debitAccount is None

    def test_mapTransactions_ignoredCategory_empty(self):
        # arrange
        transactions = [
            Transaction("Einlagen", "Deposit", datetime(
                2025, 7, 15), None, None, 100.00)
        ]

        # act
        result = list(self.testee.mapTransactions(transactions))

        # assert
        assert len(result) == 0

    def test_mapTransactions_ignoredPattern_empty(self):
        # arrange
        transactions = [
            Transaction("Essen & Trinken", "PAYMENT - THANK YOU",
                        datetime(2025, 7, 15), None, None, 100.00)
        ]

        # act
        result = list(self.testee.mapTransactions(transactions))

        # assert
        assert len(result) == 0

    def test_mapTransactions_multipleTransactions_multipleEntries(self):
        # arrange
        transactions = [
            Transaction("Essen & Trinken", "Restaurant",
                        datetime(2025, 7, 15), None, None, 25.50),
            Transaction("Transport", "SBB CFF FFS", datetime(
                2025, 7, 16), None, None, 15.00),
            Transaction("Unknown", "Store", datetime(
                2025, 7, 17), None, None, 50.00)
        ]

        # act
        result = list(self.testee.mapTransactions(transactions))

        # assert
        assert len(result) == 3
        assert result[0].mappedDescription == "Verpflegung"
        assert result[1].mappedDescription == "Öffentlicher Verkehr"
        assert result[2].mappedDescription == "Store"

    def test_mapGroups_mappedCategory_bookingEntry(self):
        # arrange
        group = Group(
            category="Essen & Trinken",
            totalAmount=100.50,
            transactionCount=3,
            monthEndDate=datetime(2025, 7, 31),
            transactions=[]
        )

        # act
        result = list(self.testee.mapGroups([group]))

        # assert
        assert len(result) == 1
        entry = result[0]
        assert entry.mappedDescription == "Verpflegung"
        assert entry.debitAccount == "5821"
        assert entry.creditAccount == "2110"
        assert entry.group == group
        assert entry.transaction is None

    def test_mapGroups_unmappedCategory_bookingEntryWithoutDebit(self):
        # arrange
        group = Group(
            category="Unknown",
            totalAmount=50.00,
            transactionCount=1,
            monthEndDate=datetime(2025, 7, 31),
            transactions=[]
        )

        # act
        result = list(self.testee.mapGroups([group]))

        # assert
        assert len(result) == 1
        entry = result[0]
        assert entry.mappedDescription == "Unknown"
        assert entry.debitAccount is None

    def test_mapGroups_multipleGroups_multipleEntries(self):
        # arrange
        groups = [
            Group("Essen & Trinken", 100.50, 3, datetime(2025, 7, 31), []),
            Group("Unknown", 50.00, 1, datetime(2025, 7, 31), [])
        ]

        # act
        result = list(self.testee.mapGroups(groups))

        # assert
        assert len(result) == 2
        assert result[0].mappedDescription == "Verpflegung"
        assert result[1].mappedDescription == "Unknown"
