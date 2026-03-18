# Transaction Processing Requirements

## Overview

The system must intelligently process, filter, group, and map credit card transactions for accounting purposes.

## Filtering

- **Early filtering**: Ignored transactions are excluded before any processing
- **Category and Transaction Based Filtering**: Skip entire categories (e.g., "Einlagen" - deposits) or specific transations (e.g., "Ihre Zahlung - Danke" - payments)
- **Configurable**: Categories and transactions to ignore defined in configuration file
- **Flexible Matching**: Support case-insensitive, regular expression matching for transaction descriptions

## Grouping

The system must consolidate transactions for accounting efficiency:

- **Configurable Mapping**: Category-to-account mapping via JSON configuration file
- **Mapping Key = Source Category**: Each key in the JSON `mapping` object corresponds to a category from the Viseca source data
- **Group by Mapping Rule**: Transactions matching the same mapping rule (same description + debit account) are grouped together, regardless of their source category
- **Cross-Category Pattern Matching**: When a transaction's source category has no applicable rule (no mapping key, or no matching pattern and no catch-all), patterns from all mapping rules are tried. Matched transactions join the same group as direct category matches for that rule
- **TRX-ID as Category**: Viseca sometimes exports a transaction ID (e.g. `TRX123245678`) instead of a category name. These transactions must still be matched via cross-category pattern fallback and grouped correctly
- **Representative Date**: Use months last day as date for the grouped entry
- **Consolidated Output**: One line per group instead of multiple lines per transaction
- **Flexible Matching**: Support case-insensitive, regular expression matching for categories
- **Mapped Categories Only**: Only transactions with valid category mapping are grouped
- **Currency Consistency**: Only CHF amounts are summed (foreign currency preserved separately)
- **Sum Amounts**: All amounts within a group are summed
- **Debit Account**: Use configured categories account
- **Credit Account**: Use configured global credit account
- **Description**: Use configured category description for the group

## Ungrouped Transactions

- **No Grouping**: Unmapped transactions are not grouped or summed
- **Individual Lines**: Each unmapped transaction gets a separate output line
- **Date**: Use original date
- **Debit Account**: Leave debit account blank for manual assignment
- **Credit Account**: Use configured global credit account
- **Description**: Use original description

## Example Processing Flow

**Input Transactions:**

```text
Essen & Trinken: 4.30 CHF + 18.50 CHF + 10.00 CHF
Fahrzeug: 85.25 CHF  
SBB CFF FFS: 6.40 CHF
Einlagen: -157.95 CHF (ignored - category)
Ihre Zahlung - Danke: -50.00 CHF (ignored - transaction)
RentACar: 155.95 CHF (unmapped)
```

**Processing Result:**

```text
- Filtered out: "Einlagen" and "Ihre Zahlung - Danke"
- Grouped: "Essen & Trinken" → "Verpflegung" (32.80 CHF)
- Mapped: "Fahrzeug" → "Auto; Diesel" (85.25 CHF)
- Mapped: "SBB CFF FFS" → "Öffentlicher Verkehr" (6.40 CHF)  
- Individual: "RentACar" (155.95 CHF, empty debit account)
```

## Validation Requirements

### Data Integrity

- **Amount Verification**: Verify that total output amounts match processed input amounts
- **Completeness Check**: Ensure no transactions are lost during processing
- **Configuration Validation**: Validate configuration file structure and content

### Error Handling

- **Missing Mappings**: Clear reporting of unmapped categories
- **Invalid Amounts**: Handle malformed amount data gracefully
- **Configuration Errors**: Provide clear error messages for configuration issues
