# Input Format Specification

## Viseca Credit Card Exports

### Export Process
- **Source**: Viseca/Migros Cumulus credit card web portal
- **Method**: Browser "Save as Text" function on transaction pages
- **Frequency**: Monthly statements require multiple page exports
- **File Format**: Plain text files containing transaction data

### File Characteristics
- **Content**: Monthly credit card transaction history
- **Structure**: Each page of the monthly statement becomes one text file
- **Size**: Small files typical of browser text exports
- **Encoding**: Standard UTF-8 text format

## Transaction Data Content

### Available Information
Each transaction in the text export contains:

- **Date and Time**: When the transaction occurred
- **Merchant Name**: Where the transaction took place
- **Location**: City or place of transaction (when available)
- **Amount**: Transaction amount in CHF or foreign currency
- **Category**: Type of expense (food, transport, shopping, etc.)

### Transaction Categories
The system recognizes these expense categories:
- **Essen & Trinken** (Food & Beverages)
- **Fahrzeug** (Vehicle/Fuel)
- **Shopping** (Retail purchases)
- **Transport** (SBB/Railway)
- **Allgemeines** (General expenses)
- **Gebühren** (Fees)
- **Einlagen** (Payments/Credits)

### Multi-Currency Transactions
- **Base Currency**: All transactions have amounts in CHF (Swiss Francs)
- **Foreign Currency**: When present, foreign currency amounts are additional information only
- **Typical Pattern**: Transaction shows both CHF amount and original foreign currency
- **Usage**: Foreign currency information should be preserved in output remarks column
- **Scope**: Only CHF and foreign currencies (primarily EUR) - no complex multi-currency scenarios

### Data Limitations
- Text format is unstructured (not CSV or standard format)
- Monthly statements span multiple files requiring manual export
- Some transactions may have incomplete location information
- Format depends on web portal layout and may change over time