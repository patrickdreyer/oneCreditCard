# Output Format Specification

## OpenOffice Calc Accounting Format

### Purpose
Generate standardized accounting journal entries in OpenOffice Calc (.ods) format suitable for CFO bookkeeping workflows. The output format is configurable via configuration file to accommodate different accounting systems.

### File Structure
Each monthly statement produces one ODS file containing all transactions for that month, regardless of how many input text files were processed.

### Configurable Column Structure
The output spreadsheet column structure is defined in the configuration file. Core columns use a `type` field, while compatibility columns are defined without a `type`.

**Default configuration for Banana accounting:**
| Position | Type | Default Name | Purpose | Example Data | Notes |
|----------|------|--------------|---------|--------------|-------|
| A | date | Datum | Transaction date | 31.07.25 | Core |
| B | description | Beschreibung | Expense category | Verpflegung | Core |
| C | debit_account | KtSoll | Debit account code | 5821 | Core |
| D | credit_account | KtHaben | Credit account code | 2110 | Core |
| E | amount_chf | Betrag CHF | Amount in Swiss Francs | 397.75 | Core |
| F | - | Saldo | Balance (always empty) | | Optional |
| G | - | KS1 | Cost center 1 (always empty) | | Optional |
| H | - | KS2 | Cost center 2 (always empty) | | Optional |
| I | - | KS3 | Cost center 3 (always empty) | | Optional |
| J | remarks | Bemerkungen | Comments/Notes | EUR 594.00 | Core |

### Core Columns (With Type)
These columns have a `type` field and are essential for the tool's functionality:
- **date**: Transaction date
- **description**: Categorized transaction description  
- **debit_account**: Debit account code from account mapping
- **credit_account**: Credit account code from account mapping
- **amount_chf**: Transaction amount in CHF
- **remarks**: Multi-currency information and notes

### Optional Columns (No Type)
These columns have no `type` field and are added for compatibility or formatting:
- **name**: Column name only
- **always_empty**: Can be set to true for empty placeholder columns
- **Purpose**: Enable exact format matching for target applications

## Data Format Requirements

### Configuration-Based Formatting
All data formatting rules are defined in the configuration file, including:
- Column names and positions
- Date format specifications
- Data mapping rules
- Multi-currency handling

### Date Format
- Configurable format (default: DD.MM.YY two-digit year)
- Example: Transaction on 31.07.2025 becomes "31.07.25"
- Format specified in configuration file

### Transaction Descriptions
Map transaction categories to accounting descriptions via configuration file:
- Category recognition patterns
- Description text mapping
- Default descriptions for unmapped categories

### Account Codes
Account mapping is defined in the configuration file and maps transaction categories to accounting codes.

**Configuration Requirements:**
- Account codes must be configurable via configuration file
- Each transaction category maps to specific debit and credit accounts
- Default account codes for unmapped transactions
- Flexible account code formats (numeric, alphanumeric)

### Amount Handling
- All amounts in the "Betrag CHF" column must be in Swiss Francs
- Use decimal format (e.g., 397.75, not 397,75)

### Multi-Currency Transactions
- **Base Currency**: All amounts in "Betrag CHF" column are in Swiss Francs
- **Foreign Currency Information**: Original foreign currency amounts stored in "Bemerkungen" column
- **Format**: "EUR 594.00" (currency code followed by amount)
- **Processing**: No currency conversion required - CHF amount is always provided in input
- **Scope**: Limited to CHF as base currency with occasional foreign currency reference information

### Empty Columns for Application Compatibility
Compatibility columns that remain empty but enable seamless data import:
- **Saldo (Balance)**: Always empty but enables direct copy&paste into Banana accounting
- **KS1, KS2, KS3 (Cost Centers)**: Always empty but maintain column structure for target application

**Purpose**: These compatibility columns ensure the exact format expected by specific accounting applications, enabling 1:1 copy&paste operations without manual column adjustments.

## File Naming
- Use format: YYYY-MM.ods
- Example: "2025-07.ods" for July 2025 transactions
- One file per month regardless of number of input files

## Expected Output Sample
```
Datum     | Beschreibung        | KtSoll | KtHaben | Betrag CHF | Saldo | KS1 | KS2 | KS3 | Bemerkungen
31.07.25  | Verpflegung        | 5821   | 2110    | 397.75     |       |     |     |     |
31.07.25  | SBB                | 6282   | 2110    | 29.20      |       |     |     |     |
31.07.25  | Auto; Diesel       | 6210   | 2110    | 90.70      |       |     |     |     |
31.07.25  | SCC; company 2025-07| 4400   | 2110    | 570.10     |       |     |     |     | EUR 594.00
```