# Input Format Specification

## Viseca Text Export Format

### Export Process
- **Method**: Browser "Save as Text" from Viseca web portal pages
- **Source**: Credit card transaction pages from Viseca/Migros Cumulus portal
- **File Structure**: Monthly statements split across multiple text files (one per page)
- **File Size**: Small files from browser text exports (no performance concerns)

### Text Format Characteristics
- **Type**: Unstructured text with embedded transaction data
- **Encoding**: UTF-8 from browser export
- **Structure**: Web page content saved as plain text
- **Anonymization**: Test data contains anonymized merchant names and amounts

## Transaction Data Patterns

### Data Extraction Patterns
Transaction data is embedded within web page text using specific patterns:

#### Merchant Name
- **Pattern**: Merchant name enclosed in asterisks
- **Example**: `*Gasstation 1*`, `*- My Lunch Place*`, `*SBB CFF FFS*`
- **Location**: Following the category line

#### Date and Time
- **Pattern**: DD.MM.YYYY HH:MM format
- **Example**: `31.07.2025 15:34`, `28.07.2025 20:57`
- **Location**: Following merchant name

#### Location
- **Pattern**: City name following date/time
- **Example**: `Winterthur`, `Olten`, `Bern`, `Zug`
- **Note**: Some transactions may not have location data

#### Amount
- **Pattern**: Amount enclosed in asterisks with currency
- **Example**: `*85.25* CHF`, `*4.30* CHF`
- **Location**: Following date/time and location

#### Multi-Currency Transactions
- **Pattern**: Two amounts with different currencies
- **Example**: `*285.05* CHF 297.00 EUR`
- **Note**: Original currency amount should be preserved

#### Category
- **Pattern**: Category name preceding merchant information
- **Examples**: 
  - `Fahrzeug` (Vehicle)
  - `Essen & Trinken` (Food & Drink)
  - `Allgemeines` (General)
  - `Shopping`
  - `TRX123245678` (Transaction ID)
  - `Einlagen` (Deposits/Payments)

#### Transaction URLs
- **Pattern**: URLs to transaction details
- **Example**: `<https://one.viseca.ch/de/transaktionen/detail/TRX123245678>`
- **Note**: Should be ignored during parsing

## Sample Transaction Block
```
Fahrzeug

*Gasstation 1*
31.07.2025 15:34 Winterthur
*85.25*  CHF
<https://one.viseca.ch/de/transaktionen/detail/TRX123245678>
```

## Parsing Challenges
- **Unstructured Format**: Data not in standard delimited format
- **Variable Spacing**: Inconsistent whitespace between elements
- **Mixed Content**: Transaction data mixed with web page navigation elements
- **Multi-line Records**: Single transactions span multiple lines
- **Optional Fields**: Some transactions may lack location or other details