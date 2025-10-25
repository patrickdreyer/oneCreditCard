# Transaction Processing Requirements

## Overview

The system must intelligently process, filter, group, and map credit card transactions for accounting purposes.

## Transaction Filtering Requirements

### Ignore Categories

The system must support complete exclusion of transaction categories:

- **Category-Based Filtering**: Skip entire categories (e.g., "Einlagen" - deposits)
- **Complete Exclusion**: Ignored categories do not appear in output
- **Configurable**: Categories to ignore defined in configuration file

### Ignore Specific Transactions  

The system must support exclusion of specific transaction descriptions:

- **Transaction-Based Filtering**: Skip specific descriptions (e.g., "Ihre Zahlung - Danke" - payments)
- **Pattern Matching**: Support exact text matching for transaction descriptions
- **Complete Exclusion**: Ignored transactions do not appear in output

### Filter Priority

- **Ignore takes precedence**: If a transaction matches both ignore and mapping rules, it will be ignored
- **Early filtering**: Ignored transactions are excluded before any processing

## Transaction Grouping Requirements

### Category-Based Grouping

The system must consolidate transactions for accounting efficiency:

- **Group by Category**: Transactions with same mapped category are grouped together
- **Sum Amounts**: All amounts within a group are summed
- **Representative Date**: Use appropriate date for the grouped entry
- **Consolidated Output**: One line per group instead of multiple lines per transaction

### Grouping Rules

- **Mapped Categories Only**: Only transactions with valid category mapping are grouped
- **Same Description**: Transactions must map to the same accounting description
- **Same Account Codes**: Transactions must map to the same debit and credit accounts
- **Currency Consistency**: Only CHF amounts are summed (foreign currency preserved separately)

## Account Code Mapping Requirements

### Category to Account Mapping

The system must map transaction categories to accounting codes:

- **Configurable Mapping**: Category-to-account mapping via JSON configuration file
- **Debit Account Assignment**: Map categories to appropriate expense accounts
- **Credit Account Assignment**: Uniform credit card liability account for all transactions
- **Description Generation**: Generate standardized accounting descriptions from categories

### Mapping Structure

- **One-to-One Mapping**: Each category maps to one debit account and description
- **Global Credit Account**: Single credit account used for all transactions
- **Flexible Keys**: Support case-insensitive and whitespace-flexible category matching

## Unmapped Transaction Handling Requirements

### Individual Processing

The system must handle transactions that cannot be categorized:

- **No Grouping**: Unmapped transactions are not grouped or summed
- **Individual Lines**: Each unmapped transaction gets a separate output line
- **Preserve Original**: Keep original category name as description
- **Manual Review**: Flag unmapped transactions for manual account assignment

### Account Assignment for Unmapped

- **Empty Debit Account**: Leave debit account blank for manual assignment
- **Global Credit Account**: Use the same credit account as mapped transactions
- **Original Description**: Use original Viseca category as description

## Processing Priority and Flow

1. **Filter Ignored**: Remove ignored categories and transactions first
2. **Identify Mappable**: Separate transactions that can be mapped from unmapped
3. **Group Mapped**: Group and sum transactions with valid mappings
4. **Process Unmapped**: Handle unmapped transactions individually
5. **Combine Results**: Merge grouped and individual transactions for output

## Example Processing Flow

**Input Transactions:**

```text
Essen & Trinken: 4.30 CHF + 18.50 CHF + 10.00 CHF
Fahrzeug: 85.25 CHF  
SBB CFF FFS: 6.40 CHF
Einlagen: -157.95 CHF (ignored - category)
Ihre Zahlung - Danke: -50.00 CHF (ignored - transaction)
Unbekannte Kategorie: 15.60 CHF (unmapped)
```

**Processing Result:**

```text
- Filtered out: "Einlagen" and "Ihre Zahlung - Danke"
- Grouped: "Essen & Trinken" → "Verpflegung" (32.80 CHF)
- Mapped: "Fahrzeug" → "Auto; Diesel" (85.25 CHF)
- Mapped: "SBB CFF FFS" → "Öffentlicher Verkehr" (6.40 CHF)  
- Individual: "Unbekannte Kategorie" (15.60 CHF, empty debit account)
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
