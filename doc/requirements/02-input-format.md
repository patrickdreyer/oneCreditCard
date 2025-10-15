# Input Format Specification

This document specifies the input data format from the user perspective.

## Export Process

- **Source**: Viseca/Migros Cumulus credit card web portal
- **Method**: Browser "Save as Text" function from monthly statement pages
- **Output**: Unstructured text files (not CSV or standardized format)
- **Pages**: Monthly statements split across multiple text files (one file per page)

## File Characteristics

- **Content**: Monthly credit card transaction history
- **Format**: Unstructured text with embedded transaction data
- **Encoding**: UTF-8 (standard browser export)
- **Extensions**: .txt files
- **Naming**: User-defined (typically includes month/year)
- **Multiple Files**: Each page of web portal saved as separate text file

## Available Information

Each transaction contains the following data embedded in text:

- **Date**: Transaction date
- **Amount**: Transaction amount in CHF (Swiss Francs)
- **Merchant**: Merchant name and location
- **Category**: Transaction category (see list below)
- **Foreign Currency**: Original amount if transaction was in foreign currency

## Transaction Categories

Categories found in Viseca exports:

- **Essen & Trinken** (Food & Beverages)
- **Fahrzeug** (Vehicle/Transport)
- **Einkauf** (Shopping)
- **Gesundheit** (Health)
- **Diverses** (Miscellaneous)
- **Dienstleistung** (Services)

## Multi-Currency Transactions

- **Base Currency**: All transactions have amounts in CHF (Swiss Francs)
- **Foreign Currency**: Original foreign currency amount and exchange rate may be present in text
- **Conversion**: CHF amount represents the final charged amount after conversion
- **Remark**: Foreign currency information should be preserved in remarks column of output

## Data Limitations

- Text format is unstructured (not CSV or standard format)
- Transaction data embedded within web page text exports
- Requires regex parsing to extract structured data
- Format depends on web portal layout and may change over time
