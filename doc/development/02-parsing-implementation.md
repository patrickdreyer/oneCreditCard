# Text Parsing Implementation

## Viseca Text Export Parsing

### Regex Patterns

- **Regex Patterns**: Use compiled regex for performance
- **Multi-line Matching**: Handle transactions spanning multiple lines
- **Error Tolerance**: Graceful handling of parsing failures
- **Data Validation**: Verify extracted data completeness and format

#### Transaction Block Pattern

```python
# Multi-line transaction pattern
TRANSACTION_PATTERN = re.compile(r'''
    (?P<category>[^\n*]+)\n\n        # Category line
    \*(?P<merchant>[^*]+)\*\n        # Merchant in asterisks
    (?P<date>\d{2}\.\d{2}\.\d{4})\s  # Date DD.MM.YYYY
    (?P<time>\d{2}:\d{2})\s          # Time HH:MM
    (?P<location>[^\n]*)\n           # Optional location
    \*(?P<amount>\d+\.\d{2})\*\s     # Amount in asterisks
    (?P<currency>CHF|EUR)            # Currency
    (?:\s(?P<foreign_amount>\d+\.\d{2})\s(?P<foreign_currency>CHF|EUR))? # Optional foreign currency
''', re.VERBOSE | re.MULTILINE)
```

#### Individual Data Patterns

```python
# Merchant name extraction
MERCHANT_PATTERN = re.compile(r'\*([^*]+)\*')

# Date extraction
DATE_PATTERN = re.compile(r'(\d{2}\.\d{2}\.\d{4})\s(\d{2}:\d{2})')

# Amount extraction
AMOUNT_PATTERN = re.compile(r'\*(\d+\.\d{2})\*\s+(CHF|EUR)')

# Multi-currency detection
MULTI_CURRENCY_PATTERN = re.compile(r'\*(\d+\.\d{2})\*\s+CHF\s+(\d+\.\d{2})\s+(EUR)')
```

### Parsing Strategy

#### Text Preprocessing

1. **Normalize Whitespace**: Convert multiple spaces to single spaces
2. **Line Ending Normalization**: Ensure consistent line endings
3. **Encoding Handling**: Process UTF-8 text from browser exports
4. **Navigation Removal**: Filter out web page navigation elements

#### Transaction Extraction Process

1. **Category Detection**: Identify transaction category lines
2. **Block Extraction**: Extract complete transaction blocks
3. **Field Parsing**: Parse individual fields from blocks
4. **Validation**: Verify extracted data completeness
5. **Error Handling**: Log parsing failures and continue processing

### Category Mapping

```python
CATEGORY_PATTERNS = {
    'essen_trinken': re.compile(r'Essen & Trinken', re.IGNORECASE),
    'fahrzeug': re.compile(r'Fahrzeug', re.IGNORECASE),
    'shopping': re.compile(r'Shopping', re.IGNORECASE),
    'transport': re.compile(r'SBB|Transport', re.IGNORECASE),
    'allgemeines': re.compile(r'Allgemeines', re.IGNORECASE),
    'einlagen': re.compile(r'Einlagen', re.IGNORECASE),
}
```

### Error Handling

#### Common Parsing Issues

- **Incomplete Transactions**: Missing merchant, date, or amount
- **Format Variations**: Slight changes in web portal output
- **Multi-line Merchants**: Merchant names spanning multiple lines
- **Special Characters**: Unicode handling in merchant names

#### Recovery Strategies

- **Partial Data**: Accept transactions with optional missing fields
- **Fallback Patterns**: Alternative regex patterns for format variations
- **Manual Review**: Flag unparseable transactions for manual processing
- **Logging**: Detailed logs for debugging parsing issues

### Performance Considerations

#### Optimization Techniques

- **Compiled Patterns**: Pre-compile all regex patterns
- **Chunked Processing**: Process large files in chunks
- **Memory Management**: Stream processing for large datasets
- **Caching**: Cache compiled patterns and category mappings

#### Scalability

- **Parallel Processing**: Process multiple files concurrently
- **Incremental Processing**: Support partial file processing
- **Progress Tracking**: Provide progress feedback for large operations