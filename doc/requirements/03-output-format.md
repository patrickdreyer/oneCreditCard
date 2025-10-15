# Output Format Specification

## OpenOffice Calc (.ods) Format

### Column Structure
The output ODS files must follow this exact column structure:

| Column | German Name | Purpose | Example |
|--------|-------------|---------|---------|
| A | Datum | Transaction date | 31.07.25 |
| B | Beschreibung | Transaction description | Verpflegung |
| C | KtSoll | Debit account code | 5821 |
| D | KtHaben | Credit account code | 2110 |
| E | Betrag CHF | Amount in CHF | 397.75 |
| F | Saldo | Balance (typically empty) | |
| G | KS1 | Cost center 1 (typically empty) | |
| H | KS2 | Cost center 2 (typically empty) | |
| I | KS3 | Cost center 3 (typically empty) | |
| J | Bemerkungen | Remarks/Comments | EUR 594.00 |

### Data Format Requirements

#### Date Format
- **Format**: DD.MM.YY (two-digit year)
- **Examples**: `31.07.25`, `28.08.25`, `13.09.25`
- **Source**: Convert from DD.MM.YYYY HH:MM in input text

#### Description (Beschreibung)
- **Content**: Categorized transaction description
- **Examples**:
  - `Verpflegung` (Food/Meals)
  - `SBB` (Swiss Federal Railways)
  - `Auto; Diesel` (Vehicle; Diesel)
  - `Gebühren` (Fees)
  - `SCC; company 2025-07` (Shopping; company with period)

#### Account Codes (KtSoll/KtHaben)
Account mapping based on transaction category:

| Category | Description | KtSoll (Debit) | KtHaben (Credit) |
|----------|-------------|----------------|------------------|
| Verpflegung | Food & Meals | 5821 | 2110 |
| SBB | Transport/Railway | 6282 | 2110 |
| Auto/Diesel | Vehicle/Fuel | 6210 | 2110 |
| SCC/Shopping | Shopping/Purchases | 4400 | 2110 |
| Gebühren | Fees | 6940 | 2110 |

**Note**: KtHaben (Credit) is consistently 2110 for credit card transactions.

#### Amount (Betrag CHF)
- **Format**: Decimal number with CHF as base currency
- **Examples**: `397.75`, `29.20`, `90.70`, `2.00`
- **Source**: Extract from `*XX.XX* CHF` pattern in input text

#### Multi-Currency Handling
- **Primary Amount**: Always in CHF in the Betrag CHF column
- **Original Currency**: Store in Bemerkungen column if different
- **Format Example**: `EUR 594.00` in Bemerkungen column
- **Note**: Conversion rates need to be handled externally

## Sample Output Rows

### Header Row
```
Datum | Beschreibung | KtSoll | KtHaben | Betrag CHF | Saldo | KS1 | KS2 | KS3 | Bemerkungen
```

### Data Rows Examples
```
31.07.25 | Verpflegung | 5821 | 2110 | 397.75 | | | | |
31.07.25 | SBB | 6282 | 2110 | 29.20 | | | | |
31.07.25 | Auto; Diesel | 6210 | 2110 | 90.70 | | | | |
31.07.25 | SCC; company 2025-07 | 4400 | 2110 | 570.10 | | | | | EUR 594.00
```

## File Naming Convention
- **Pattern**: `YYYY-MM.ods`
- **Examples**: `2025-07.ods`, `2025-08.ods`, `2025-09.ods`
- **Note**: Derived from transaction dates in input files

## Empty Columns
- **Saldo**: Typically left empty
- **KS1, KS2, KS3**: Cost center columns, typically left empty
- **Bemerkungen**: Used only for multi-currency information