import re
from dataclasses import dataclass
from typing import Iterator, List, Optional

from parsers.transaction import Transaction
from configuration import Configuration, MappingRule
from transactionGrouper import Group
from logging_config import getLogger

logger = getLogger(__name__)


@dataclass
class BookingEntry:
    mappedDescription: str
    debitAccount: Optional[str]
    creditAccount: str
    transaction: Optional[Transaction] = None
    group: Optional[Group] = None


class AccountMapper:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration

    def mapTransactions(self, transactions: List[Transaction]) -> Iterator[BookingEntry]:
        # Maps transactions to account codes and descriptions based on configuration
        mappedCount = 0
        unmappedCount = 0
        ignoredCount = 0

        for transaction in transactions:
            if self.__ignored(transaction):
                ignoredCount += 1
                logger.debug("Transaction ignored; merchant='%s', category='%s'",
                            transaction.merchant, transaction.category)
                continue

            mappingRule = self.__findMappingRule(transaction)
            if mappingRule:
                # Create mapped transaction with mapping information
                mappedCount += 1
                logger.debug("Transaction mapped; merchant='%s', category='%s', description='%s', debitAccount='%s'",
                            transaction.merchant, transaction.category,
                            mappingRule.description, mappingRule.debitAccount)
                yield BookingEntry(
                    mappedDescription=mappingRule.description,
                    debitAccount=mappingRule.debitAccount,
                    creditAccount=self.configuration.creditAccount,
                    transaction=transaction
                )
            else:
                # Unmapped transaction - use merchant as description, no debit account
                unmappedCount += 1
                logger.debug("Transaction unmapped; merchant='%s', category='%s'",
                            transaction.merchant, transaction.category)
                yield BookingEntry(
                    mappedDescription=transaction.merchant,
                    debitAccount=None,
                    creditAccount=self.configuration.creditAccount,
                    transaction=transaction
                )

        logger.info("Transactions mapped; total=%d, mapped=%d, unmapped=%d, ignored=%d",
                   len(transactions), mappedCount, unmappedCount, ignoredCount)

    def mapGroups(self, groups: List[Group]) -> Iterator[BookingEntry]:
        # Map grouped transactions
        mappedCount = 0
        unmappedCount = 0

        for group in groups:
            mappingRule = group.mappingRule or self.__findMappingRuleByCategory(group.category)
            if mappingRule:
                mappedCount += 1
                logger.debug("Group mapped; category='%s', description='%s', debitAccount='%s', transactions=%d",
                            group.category, mappingRule.description,
                            mappingRule.debitAccount, len(group.transactions))
                yield BookingEntry(
                    mappedDescription=mappingRule.description,
                    debitAccount=mappingRule.debitAccount,
                    creditAccount=self.configuration.creditAccount,
                    group=group
                )
            else:
                # This shouldn't happen if grouping is correct, but handle it
                unmappedCount += 1
                logger.debug("Group unmapped; category='%s', transactions=%d",
                            group.category, len(group.transactions))
                yield BookingEntry(
                    mappedDescription=group.category,
                    debitAccount=None,
                    creditAccount=self.configuration.creditAccount,
                    group=group
                )

        logger.info("Groups mapped; total=%d, mapped=%d, unmapped=%d",
                   len(groups), mappedCount, unmappedCount)

    def __ignored(self, transaction: Transaction) -> bool:
        return self.__ignoredCategory(transaction) or self.__ignoredTransaction(transaction)

    def __ignoredCategory(self, transaction: Transaction) -> bool:
        for ignoredCategory in self.configuration.ignoreRules.categories:
            if transaction.category.lower() == ignoredCategory.lower():
                return True
        return False

    def __ignoredTransaction(self, transaction: Transaction) -> bool:
        for ignoredTransaction in self.configuration.ignoreRules.transactions:
            if self.__matchesPattern(transaction.merchant, ignoredTransaction):
                return True
        return False

    def __findMappingRule(self, transaction: Transaction) -> Optional[MappingRule]:
        mappingRules = self.configuration.mappingRules

        # Direct category match: check patterns first, then fall back to catch-all
        if transaction.category in mappingRules:
            catchAll: Optional[MappingRule] = None
            for rule in mappingRules[transaction.category]:
                if rule.pattern:
                    if self.__matchesPattern(transaction.merchant, rule.pattern):
                        return rule
                elif catchAll is None:
                    catchAll = rule
            return catchAll

        # No direct category match, check pattern matching for all rules
        for rules in mappingRules.values():
            for rule in rules:
                if rule.pattern and self.__matchesPattern(transaction.merchant, rule.pattern):
                    return rule

        return None

    def __findMappingRuleByCategory(self, category: str) -> Optional[MappingRule]:
        mappingRules = self.configuration.mappingRules
        rules = mappingRules.get(category)
        if not rules:
            return None
        # Return the catch-all rule (no pattern) if available
        for rule in rules:
            if not rule.pattern:
                return rule
        return None

    def __matchesPattern(self, text: str, pattern: str) -> bool:
        return re.search(pattern, text, re.IGNORECASE) is not None
