from calendar import monthrange
from dataclasses import dataclass, field
from datetime import datetime
import re
from typing import Dict, Iterator, List, Optional, Tuple

from configuration import Configuration, MappingRule
from logging_config import getLogger
from parsers.transaction import Transaction

logger = getLogger(__name__)


@dataclass
class Group:
    description: str
    totalAmount: float
    transactionCount: int
    monthEndDate: datetime
    transactions: List[Transaction]
    mappingRule: Optional[MappingRule] = field(default=None)


class TransactionGrouper:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration

    def group(self, transactions: Iterator[Transaction]) -> Tuple[List[Transaction], List[Group]]:
        # key: (description, debitAccount) to group by mapping rule, not source category
        toBeGrouped: Dict[Tuple[str, str], Dict] = {}
        individual = []
        for transaction in transactions:
            rule = self.__findMatchingRule(transaction)
            if rule:
                key = (rule.description, rule.debitAccount)
                if key not in toBeGrouped:
                    toBeGrouped[key] = {'rule': rule, 'transactions': []}
                toBeGrouped[key]['transactions'].append(transaction)
                logger.debug("Transaction added to group; merchant='%s', category='%s', debitAccount='%s'",
                            transaction.merchant, transaction.category, rule.debitAccount)
            else:
                individual.append(transaction)
                logger.debug("Transaction kept individual; merchant='%s', category='%s'",
                            transaction.merchant, transaction.category)

        groups = []
        for (description, _), entry in toBeGrouped.items():
            rule = entry['rule']
            groupTransactions = entry['transactions']
            totalAmount = sum(t.amount for t in groupTransactions)
            monthEndDate = self.__getMonthEndDate(groupTransactions[0].date)
            groups.append(
                Group(
                    description=description,
                    totalAmount=totalAmount,
                    transactionCount=len(groupTransactions),
                    monthEndDate=monthEndDate,
                    transactions=groupTransactions,
                    mappingRule=rule,
                )
            )
            logger.debug("Group created; description='%s', debitAccount='%s', transactions=%d, totalAmount=%.2f",
                        description, rule.debitAccount, len(groupTransactions), totalAmount)

        return individual, groups

    def __findMatchingRule(self, transaction: Transaction) -> Optional[MappingRule]:
        mappingRules = self.configuration.mappingRules

        # Pass 1: direct category match — check patterns first, then catch-all
        if transaction.category in mappingRules:
            catchAll: Optional[MappingRule] = None
            for rule in mappingRules[transaction.category]:
                if rule.pattern:
                    if self.__matchesPattern(transaction.merchant, rule.pattern):
                        return rule
                elif catchAll is None:
                    catchAll = rule
            if catchAll:
                return catchAll

        # Pass 2: pattern-based matching across all categories
        for rules in mappingRules.values():
            for rule in rules:
                if rule.pattern and self.__matchesPattern(transaction.merchant, rule.pattern):
                    return rule

        return None

    def __matchesPattern(self, text: str, pattern: str) -> bool:
        try:
            return re.search(pattern, text, re.IGNORECASE) is not None
        except re.error as exc:
            logger.error("Invalid regex pattern in grouping; pattern='%s', error='%s'", pattern, exc)
            return pattern.lower() in text.lower()

    def __getMonthEndDate(self, date: datetime) -> datetime:
        lastDay = monthrange(date.year, date.month)[1]
        return datetime(date.year, date.month, lastDay)
