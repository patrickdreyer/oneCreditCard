# Output Format

## Target

OpenOffice Calc (.ods) files for accounting software import.

## Column Structure

The output format supports configurable columns with both required typed columns and optional named-only columns.

Example for Banana:

| Position | Type | Example Name | Purpose | Example Data | Notes |
|----------|------|--------------|---------|--------------|-------|
| 1 | date | Datum | Transaction date | 15.07.25 | DD.MM.YY format |
| 2 | description | Beschreibung | Accounting description | "Verpflegung" | From category mapping |
| 3 | debitAccount | KtSoll | Debit account code | "5821" | From mapping config |
| 4 | creditAccount | KtHaben | Credit account code | "2110" | From mapping config |
| 5 | amountChf | Betrag CHF | Amount in CHF | 25.50 | Always CHF |
| 6 | - | Saldo | Balance | (empty) | For easy copy&paste |
| 7 | - | KS1 | Cost center 1 | (empty) | For easy copy&paste |
| 8 | - | KS2 | Cost center 2 | (empty) | For easy copy&paste |
| 9 | - | KS3 | Cost center 3 | (empty) | For easy copy&paste |
| 10 | - | Bemerkung | Remarks/Notes | "EUR 23.45" | Foreign currency info |

## Core Columns (With Type)

- **date**: Transaction date
- **description**: Accounting description (mapped from category)
- **debitAccount**: Debit account code (from configuration)
- **creditAccount**: Credit account code (from configuration)  
- **amountChf**: Transaction amount in CHF (always Swiss Francs)

## Optional Columns (No Type)

- **name**: Column name only
- **purpose**: Display purposes, balance column, remarks, etc.
- **content**: Empty by default but may contain supplementary information

## Configuration-Based Formatting

The system must support configuration of:

- Column names and positions
- Date format patterns
- Number format for amounts
- Account code mapping rules

## Date Format

- Configurable format (default: DD.MM.YY two-digit year)
- Examples: 15.07.25, 03.08.25, 24.12.25
- Must be compatible with accounting software import requirements

## Transaction Descriptions

- **Source**: Mapped from transaction categories using configuration file
- **Examples**: "Verpflegung" (Food), "Auto; Diesel" (Vehicle)
- **Mapping**: Category recognition patterns
- **Fallback**: Unmapped transactions get empty description

## Account Codes

- **Structure**: 4-digit accounting codes as strings
- **Examples**: "5821" (expense account), "2110" (credit card liability account)
- **Debit Account**: Expense category (varies by transaction type)
- **Credit Account**: Typically credit card liability account (often same for all)
- Account codes must be configurable via configuration file

## Amount Handling

- All amounts in the "Betrag CHF" column must be in Swiss Francs
- Positive values represent expenses (typical for credit card transactions)
- Format: Decimal with 2 places (25.50, 125.00, 15.75)

## Multi-Currency

- **Base Currency**: All amounts in "Betrag CHF" column are in Swiss Francs
- **Foreign Currency Preservation**: Original foreign currency amounts preserved in "Bemerkung" (Remarks) column
- **Format**: "EUR 23.45", "USD 27.80", etc.
- **Exchange Rate**: Not required in output (CHF amount is final)
