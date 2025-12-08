from calendar import monthrange
from dataclasses import dataclass
from datetime import datetime
import re
from typing import Iterator, List, Tuple

from configuration import Configuration
from logging_config import getLogger
from parsers.transaction import Transaction

logger = getLogger(__name__)


@dataclass
class Group:
    category: str
    totalAmount: float
    transactionCount: int
    monthEndDate: datetime
    transactions: List[Transaction]


class TransactionGrouper:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration

    def group(self, transactions: Iterator[Transaction]) -> Tuple[List[Transaction], List[Group]]:
        toBeGrouped = {}
        individual = []
        for transaction in transactions:
            if self.__canGroup(transaction):
                category = transaction.category
                if category not in toBeGrouped:
                    toBeGrouped[category] = []
                toBeGrouped[category].append(transaction)
                logger.debug("Transaction added to group; merchant='%s', category='%s'",
                            transaction.merchant, category)
            else:
                individual.append(transaction)
                logger.debug("Transaction kept individual; merchant='%s', category='%s'",
                            transaction.merchant, transaction.category)

        groups = []
        for category, categoryTransactions in toBeGrouped.items():
            totalAmount = sum(t.amount for t in categoryTransactions)
            monthEndDate = self.__getMonthEndDate(categoryTransactions[0].date)
            groups.append(
                Group(
                    category=category,
                    totalAmount=totalAmount,
                    transactionCount=len(categoryTransactions),
                    monthEndDate=monthEndDate,
                    transactions=categoryTransactions,
                )
            )
            logger.debug("Group created; category='%s', transactions=%d, totalAmount=%.2f",
                        category, len(categoryTransactions), totalAmount)

        return individual, groups

    def __canGroup(self, transaction: Transaction) -> bool:
        mappingRules = self.configuration.mappingRules

        # Direct category match
        if transaction.category in mappingRules:
            rule = mappingRules[transaction.category]
            if rule.pattern:
                return self.__matchesPattern(transaction.merchant, rule.pattern)
            return True

        # Pattern-based matching
        for rule in mappingRules.values():
            if rule.pattern and self.__matchesPattern(transaction.merchant, rule.pattern):
                return True

        return False

    def __matchesPattern(self, text: str, pattern: str) -> bool:
        try:
            return re.search(pattern, text, re.IGNORECASE) is not None
        except re.error as exc:
            logger.error("Invalid regex pattern in grouping; pattern='%s', error='%s'", pattern, exc)
            return pattern.lower() in text.lower()

    def __getMonthEndDate(self, date: datetime) -> datetime:
        lastDay = monthrange(date.year, date.month)[1]
        return datetime(date.year, date.month, lastDay)
