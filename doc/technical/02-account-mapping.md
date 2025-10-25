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

## Column Configuration Rules

- **Core Columns**: Have `type` field, contain actual transaction data
- **Optional Columns**: No `type` field, used for formatting/compatibility (remain empty)
