# Account Mapping Implementation

## Purpose

Technical implementation of category-to-account mapping from JSON configuration.

## Configuration Structure

```json
{
  "creditAccount": "2110",
  "ignore": {
    "categories": ["Einlagen"],
    "transactions": ["Ihre Zahlung - Danke"]
  },
  "mapping": {
    "Essen & Trinken": {
      "description": "Verpflegung",
      "debitAccount": "5821"
    }
  },
  "columns": [
    {"name": "Datum", "type": "date", "format": "DD.MM.YY"},
    {"name": "Beschreibung", "type": "description"},
    {"name": "KtSoll", "type": "debitAccount"},
    {"name": "KtHaben", "type": "creditAccount"},
    {"name": "Betrag CHF", "type": "amountChf", "format": "decimal"},
    {"name": "Saldo"},
    {"name": "KS1"},
    {"name": "KS2"},
    {"name": "KS3"},
    {"name": "Bemerkungen", "type": "remarks"}
  ]
}
```

## Two-Pass Rule Matching

Both the `TransactionGrouper` and `AccountMapper` use the same two-pass algorithm to find a matching mapping rule for a transaction:

### Pass 1: Direct Category Match

If the transaction's source category exists as a key in the `mapping` configuration:
1. Check each rule with a `pattern` — if the merchant matches, return that rule
2. If no pattern matches, return the catch-all rule (rule without `pattern`) if one exists
3. If neither a pattern nor a catch-all matched, fall through to Pass 2

### Pass 2: Cross-Category Pattern Fallback

If the category is not in the config, or if no rule in Pass 1 matched:
1. Iterate over **all** mapping rules across **all** categories
2. For each rule with a `pattern`, test if the merchant matches
3. Return the first matching rule

This fallback is essential because Viseca sometimes exports a transaction ID (e.g. `TRX123245678`) instead of a proper category name. These transactions would never match in Pass 1, but their merchant name (e.g. "Parkingpay", "SBB CFF FFS") can still be matched via patterns defined under the correct category.

## Grouping Key

Transactions are grouped by their resolved **mapping rule** (description + debit account), not by their source category. This ensures transactions matched via cross-category pattern fallback are grouped together with direct category matches for the same rule.

## Column Configuration Rules

- **Core Columns**: Have `type` field, contain actual transaction data
- **Optional Columns**: No `type` field, used for formatting/compatibility (remain empty)
