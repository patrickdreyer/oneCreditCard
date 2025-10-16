# Input Format

## Transaction Data

Each transaction contains:

- **Date**: Transaction date
- **Amount**: Transaction amount in CHF (Swiss Francs)
- **Merchant**: Merchant name and location
- **Category**: Transaction category (see list below)
- **Foreign Currency**: Original amount if transaction was in foreign currency

## Categories

Categories found in Viseca exports:

- **Essen & Trinken** (Food & Beverages)
- **Fahrzeug** (Vehicle/Transport)
- **Einkauf** (Shopping)
- **Gesundheit** (Health)
- **Diverses** (Miscellaneous)
- **Dienstleistung** (Services)

## Multi-Currency

- **Base Currency**: All transactions have amounts in CHF (Swiss Francs)
- **Foreign Currency**: Original foreign currency amount and exchange rate may be present in text and is to be preserved in remarks column of output
