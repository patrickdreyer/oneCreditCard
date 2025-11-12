from datetime import datetime
import pytest

from src.configuration import Configuration
from src.transactionGrouper import TransactionGrouper
from src.parser.transaction import Transaction


class TestTransactionGrouper:
    @pytest.fixture(autouse=True)
    def setup(self, writeConfig):
        configData = {
            "creditAccount": "2110",
            "mapping": {
                "Essen & Trinken": {
                    "description": "Verpflegung",
                    "debitAccount": "5821"
                },
                "Transport": {
                    "description": "Öffentlicher Verkehr",
                    "debitAccount": "6282"
                }
            },
            "columns": []
        }
        config = Configuration(writeConfig("test.json", configData))
        self.testee = TransactionGrouper(config)  # pylint: disable=attribute-defined-outside-init

    def test_group_mappedCategory_grouped(self):
        # arrange
        transactions = [
            Transaction("Essen & Trinken", "Restaurant A",
                        datetime(2025, 7, 15), None, None, 25.50),
            Transaction("Essen & Trinken", "Restaurant B",
                        datetime(2025, 7, 20), None, None, 30.00)
        ]

        # act
        individual, groups = self.testee.group(iter(transactions))

        # assert
        assert len(individual) == 0
        assert len(groups) == 1
        group = groups[0]
        assert group.category == "Essen & Trinken"
        assert group.totalAmount == 55.50
        assert group.transactionCount == 2
        assert group.monthEndDate == datetime(2025, 7, 31)
        assert len(group.transactions) == 2

    def test_group_unmappedCategory_individual(self):
        # arrange
        transactions = [
            Transaction("Unknown", "Store", datetime(
                2025, 7, 15), None, None, 50.00)
        ]

        # act
        individual, groups = self.testee.group(iter(transactions))

        # assert
        assert len(individual) == 1
        assert len(groups) == 0
        assert individual[0].merchant == "Store"

    def test_group_mixedCategories_groupedAndIndividual(self):
        # arrange
        transactions = [
            Transaction("Essen & Trinken", "Restaurant",
                        datetime(2025, 7, 15), None, None, 25.50),
            Transaction("Unknown", "Store", datetime(
                2025, 7, 16), None, None, 50.00),
            Transaction("Transport", "SBB", datetime(
                2025, 7, 17), None, None, 15.00)
        ]

        # act
        individual, groups = self.testee.group(iter(transactions))

        # assert
        assert len(individual) == 1
        assert len(groups) == 2
        assert individual[0].category == "Unknown"

    def test_group_multipleTransactionsSameCategory_singleGroup(self):
        # arrange
        transactions = [
            Transaction("Essen & Trinken", "Restaurant A", datetime(2025, 7, 15), None, None, 25.50),
            Transaction("Essen & Trinken", "Restaurant B", datetime(2025, 7, 16), None, None, 30.00),
            Transaction("Essen & Trinken", "Restaurant C", datetime(2025, 7, 17), None, None, 15.50)
        ]

        # act
        _, groups = self.testee.group(iter(transactions))

        # assert
        assert len(groups) == 1
        group = groups[0]
        assert group.transactionCount == 3
        assert group.totalAmount == 71.00

    def test_group_differentMonths_correctMonthEnd(self):
        # arrange
        transactions = [
            Transaction("Essen & Trinken", "Restaurant", datetime(2025, 7, 15), None, None, 25.50)
        ]

        # act
        _, groups = self.testee.group(iter(transactions))

        # assert
        assert groups[0].monthEndDate == datetime(2025, 7, 31)

    def test_group_februaryLeapYear_correctMonthEnd(self):
        # arrange
        transactions = [
            Transaction("Essen & Trinken", "Restaurant", datetime(2024, 2, 15), None, None, 25.50)
        ]

        # act
        _, groups = self.testee.group(iter(transactions))

        # assert
        assert groups[0].monthEndDate == datetime(2024, 2, 29)

    def test_group_februaryNonLeapYear_correctMonthEnd(self):
        # arrange
        transactions = [
            Transaction("Essen & Trinken", "Restaurant", datetime(2025, 2, 15), None, None, 25.50)
        ]

        # act
        _, groups = self.testee.group(iter(transactions))

        # assert
        assert groups[0].monthEndDate == datetime(2025, 2, 28)

    def test_group_emptyTransactions_emptyResults(self):
        # arrange
        transactions = []

        # act
        individual, groups = self.testee.group(iter(transactions))

        # assert
        assert len(individual) == 0
        assert len(groups) == 0

    def test_group_patternInMappingRule_grouped(self, writeConfig):
        # arrange
        configData = {
            "creditAccount": "2110",
            "mapping": {
                "Transport": {
                    "pattern": "^SBB.*",
                    "description": "Öffentlicher Verkehr",
                    "debitAccount": "6282"
                }
            },
            "columns": []
        }
        config = Configuration(writeConfig("pattern.json", configData))
        testee = TransactionGrouper(config)
        transactions = [
            Transaction("Transport", "SBB CFF FFS", datetime(2025, 7, 15), None, None, 15.00),
            Transaction("Transport", "Taxi", datetime(2025, 7, 16), None, None, 30.00)
        ]

        # act
        individual, groups = testee.group(iter(transactions))

        # assert
        # SBB matches pattern and is mapped, so grouped
        # Taxi doesn't match pattern, not mapped, so individual
        assert len(individual) == 1
        assert len(groups) == 1
        assert individual[0].merchant == "Taxi"
        assert groups[0].transactionCount == 1
        assert groups[0].transactions[0].merchant == "SBB CFF FFS"
