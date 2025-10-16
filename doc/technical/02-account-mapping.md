# Account Mapping

## Purpose

Map Viseca categories to accounting descriptions and account codes via JSON configuration.

## Category Mapping

| Viseca Category | Description | Account |
|-----------------|-------------|---------|
| Essen & Trinken | Verpflegung | 5821 |
| Fahrzeug | Auto; Diesel | 6210 |
| Shopping | Shopping | 5800 |

## Column Configuration Rules

- **Core Columns**: Have `type` field, contain actual transaction data
- **Optional Columns**: No `type` field, used for formatting/compatibility (remain empty)

**Configuration Example:**

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

## Processing Rules

1. **Ignore**: Skip categories/transactions in ignore section
2. **Map**: Apply category mapping to account codes
3. **Group**: Sum transactions by final description
4. **Unmapped**: Process individually with empty debit account

### Ignore vs. Mapping Priority

- **Ignore takes precedence**: If a transaction matches both ignore and mapping rules, it will be ignored
- **Complete exclusion**: Ignored transactions do not appear in output at all
- **No processing**: Ignored transactions are not grouped, summed, or validated

### Unmapped Transaction Handling

For transactions that cannot be mapped to any category:

- **Individual Processing**: Each unmapped transaction becomes a separate line item
- **No Grouping**: These transactions are not summed with others
- **Account Assignment**:
  - `debitAccount`: Left empty (blank)
  - `creditAccount`: Uses global `creditAccount` from configuration
  - `description`: Original category name from Viseca export

### Global Credit Account

- **Single Value**: All transactions use the same `creditAccount` value
- **Configuration**: Defined once at top level as `creditAccount`
- **Simplification**: Removes redundancy from individual mappings
- **Exception**: Special cases like "Einlagen" may override this pattern

### Grouping and Summation

- **Mapped Transactions**: Grouped by final accounting description and summed
- **Unmapped Transactions**: Processed individually without grouping
- **Output**: One line per group (mapped) or per transaction (unmapped)
- **Details**: Original transaction information preserved in remarks if needed

### Multi-Currency Handling

- CHF amounts are summed directly
- Foreign currency information is preserved in remarks column
- No currency conversion performed (CHF amount always provided by Viseca)

## Configuration Key Format

### Category Key Format

Configuration keys use the exact Viseca category text. The matching logic handles case and whitespace variations:

| Viseca Category | Configuration Key | Matching Examples |
|-----------------|-------------------|-------------------|
| Essen & Trinken | "Essen & Trinken" | "ESSEN & trinken", "essen⎵⎵⎵&⎵⎵trinken" |
| Fahrzeug | "Fahrzeug" | "FAHRZEUG", "fahrzeug" |
| Shopping | "Shopping" | "SHOPPING", "shopping" |
| Allgemeines | "Allgemeines" | "ALLGEMEINES", "allgemeines" |
| Einlagen | "Einlagen" | "EINLAGEN", "einlagen" |
| Reisen | "Reisen" | "REISEN", "reisen" |

### Flexible Matching Logic

The system performs case-insensitive and whitespace-flexible matching:

- **Case-insensitive**: "Essen & Trinken" matches "ESSEN & trinken"
- **Whitespace-flexible**: "Essen & Trinken" matches "Essen⎵⎵⎵&⎵⎵trinken"
- **Combined**: "ESSEN⎵⎵⎵&⎵⎵trinken" matches "Essen & Trinken"

**Implementation approach:**

- Configuration keys are exact category names (e.g., "Essen & Trinken")
- Matching normalizes both input and config key for comparison only
- Original configuration structure preserved

### Account Code Format

- Account codes can be numeric (e.g., "5821") or alphanumeric
- String format recommended for flexibility
- Consistent format within each configuration

## Example Output Impact

**Input Transactions:**

```text
Essen & Trinken: 4.30 CHF + 18.50 CHF + 10.00 CHF = 32.80 CHF
Fahrzeug: 85.25 CHF
SBB CFF FFS: 6.40 CHF
Einlagen: -157.95 CHF (ignored - category)
Ihre Zahlung - Danke: -50.00 CHF (ignored - transaction)
Unbekannte Kategorie: 15.60 CHF (unmapped)
```

**Grouped Output:**

```text
Datum     | Beschreibung | KtSoll | KtHaben | Betrag CHF
31.07.25  | Verpflegung  | 5821   | 2110    | 32.80
31.07.25  | Auto; Diesel | 6210   | 2110    | 85.25  
24.07.25  | SBB          | 6282   | 2110    | 6.40
25.07.25  | Unbekannte Kategorie |    | 2110    | 15.60
```

**Note**:

- Ignored transactions ("Einlagen", "Ihre Zahlung - Danke") do not appear in output
- Unmapped transactions appear individually with empty debitAccount
