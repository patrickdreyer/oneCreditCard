import re
from dataclasses import dataclass
from typing import Iterator, List, Optional

from src.parser.transaction import Transaction
from src.configuration import Configuration, MappingRule
from src.transactionGrouper import Group


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
        for transaction in transactions:
            if self.__ignored(transaction):
                continue

            mappingRule = self.__findMappingRule(transaction)
            if mappingRule:
                # Create mapped transaction with mapping information
                yield BookingEntry(
                    mappedDescription=mappingRule.description,
                    debitAccount=mappingRule.debitAccount,
                    creditAccount=self.configuration.creditAccount,
                    transaction=transaction
                )
            else:
                # Unmapped transaction - use merchant as description, no debit account
                yield BookingEntry(
                    mappedDescription=transaction.merchant,
                    debitAccount=None,
                    creditAccount=self.configuration.creditAccount,
                    transaction=transaction
                )

    def mapGroups(self, groups: List[Group]) -> Iterator[BookingEntry]:
        # Map grouped transactions
        for group in groups:
            mappingRule = self.__findMappingRuleByCategory(group.category)
            if mappingRule:
                yield BookingEntry(
                    mappedDescription=mappingRule.description,
                    debitAccount=mappingRule.debitAccount,
                    creditAccount=self.configuration.creditAccount,
                    group=group
                )
            else:
                # This shouldn't happen if grouping is correct, but handle it
                yield BookingEntry(
                    mappedDescription=group.category,
                    debitAccount=None,
                    creditAccount=self.configuration.creditAccount,
                    group=group
                )

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

        # Direct category match
        if transaction.category in mappingRules:
            rule = mappingRules[transaction.category]
            # If rule has pattern, check if merchant matches the pattern
            if rule.pattern:
                if self.__matchesPattern(transaction.merchant, rule.pattern):
                    return rule
                # Pattern exists but doesn't match merchant, no mapping
                return None
            else:
                # No pattern, direct category match
                return rule

        # No direct category match, check pattern matching for all rules
        for rule in mappingRules.values():
            if rule.pattern and self.__matchesPattern(transaction.merchant, rule.pattern):
                return rule

        return None

    def __findMappingRuleByCategory(self, category: str) -> Optional[MappingRule]:
        mappingRules = self.configuration.mappingRules
        return mappingRules.get(category)

    def __matchesPattern(self, text: str, pattern: str) -> bool:
        return re.search(pattern, text, re.IGNORECASE) is not None
