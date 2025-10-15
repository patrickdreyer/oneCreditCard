# Account Mapping Configuration

## Transaction Grouping and Mapping Rules

The system groups transactions by category and maps them to accounting descriptions and account codes. This mapping is configured in the JSON configuration file.

## Transaction Categories from Viseca Exports

### Category-Based Mapping

Based on the "category" field in Viseca text exports:

| Viseca Category | Accounting Description | Notes |
|-----------------|----------------------|-------|
| Essen & Trinken | Verpflegung | Food and beverages |
| Fahrzeug | Auto; Diesel | Vehicle/fuel expenses |
| Shopping | Shopping | General retail purchases |
| Allgemeines | Allgemeines | General expenses |
| Einlagen | Zahlung | Payments (negative amounts) |
| Reisen | Reisen | Travel expenses |

### Merchant-Based Mapping

Some transactions require merchant-based categorization:

| Merchant Pattern | Accounting Description | Category Override |
|------------------|----------------------|------------------|
| SBB CFF FFS | SBB | Transport (regardless of Viseca category) |

## Configuration Structure

### Account Mapping Section

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
    },
    "Fahrzeug": {
      "description": "Auto; Diesel",
      "debitAccount": "6210"
    },
    "Shopping": {
      "description": "Shopping", 
      "debitAccount": "5800"
    },
    "Allgemeines": {
      "description": "Allgemeines",
      "debitAccount": "5900"
    },
    "Reisen": {
      "description": "Reisen",
      "debitAccount": "6300"
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

## Processing Logic

### Transaction Processing Priority

1. **Ignore Check**: First check if transaction should be ignored
   - Check if category matches any entry in `ignore.categories`
   - Check if transaction name matches any entry in `ignore.transactions`
   - If matched, skip transaction completely
2. **Category Mapping**: Check if category matches any entry in the `mapping` section
3. **Transaction Override**: Special handling for specific transactions (e.g., SBB CFF FFS)
4. **Unmapped Transactions**: Transactions without matching category are processed individually

### Ignore Configuration

Transactions can be excluded from processing entirely:

**Category-based Ignoring:**

- **Purpose**: Ignore entire transaction categories (e.g., payments, refunds)
- **Example**: `"categories": ["Einlagen"]` - ignores all "Einlagen" transactions
- **Matching**: Uses same flexible matching as category mapping (case-insensitive, whitespace-flexible)

**Transaction-based Ignoring:**

- **Purpose**: Ignore specific transactions regardless of category
- **Example**: `"transactions": ["Ihre Zahlung - Danke"]` - ignores this specific payment
- **Matching**: Exact transaction name matching with flexible whitespace/case handling
- **Use Case**: Filter out specific payment confirmations, refunds, or corrections

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

Examples:

- "ESSEN     & trinken" → matches config key "Essen & Trinken"
- "SBB CFF FFS" → matches config key "SBB CFF FFS"
- "fahrzeug" → matches config key "Fahrzeug"

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