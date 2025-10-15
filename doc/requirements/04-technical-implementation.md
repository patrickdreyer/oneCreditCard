# Technical Implementation Guide

## Architecture Concept

### Processing Pipeline
1. **Text File Input**: Read unstructured Viseca text exports
2. **Regex Parsing**: Extract transaction data using pattern matching
3. **Data Transformation**: Convert to accounting format with account mapping
4. **ODS Generation**: Create OpenOffice Calc files with specific structure
5. **Batch Processing**: Handle multiple input files for monthly statements

### Core Components
- **Text Parser**: Regex-based extraction from unstructured web page text
- **Transaction Processor**: Data transformation and categorization logic
- **Account Mapper**: Category-to-account-code mapping
- **ODS Generator**: OpenOffice Calc file creation using odfpy
- **CLI Interface**: Command-line interface for file processing

## Implementation Strategy

### Text Parsing Approach
- **Regex Patterns**: Use compiled regex for performance
- **Multi-line Matching**: Handle transactions spanning multiple lines
- **Error Tolerance**: Graceful handling of parsing failures
- **Data Validation**: Verify extracted data completeness and format

### Account Mapping Logic
```python
# Example mapping structure
CATEGORY_MAPPING = {
    'essen_trinken': {'description': 'Verpflegung', 'debit': '5821', 'credit': '2110'},
    'fahrzeug': {'description': 'Auto; Diesel', 'debit': '6210', 'credit': '2110'},
    'sbb': {'description': 'SBB', 'debit': '6282', 'credit': '2110'},
    'shopping': {'description': 'SCC; company', 'debit': '4400', 'credit': '2110'},
    'gebühren': {'description': 'Gebühren', 'debit': '6940', 'credit': '2110'},
}
```

### Multi-File Processing
- **File Pattern Recognition**: Identify related files for same month
- **Transaction Aggregation**: Combine transactions from multiple pages
- **Duplicate Detection**: Prevent double-processing of transactions
- **Output Consolidation**: Single ODS file per month

## Technical Risks

### High-Risk Areas
- **Regex Complexity**: Unstructured text format requires complex pattern matching
- **Format Brittleness**: Web portal export format changes could break parsing logic
- **Category Recognition**: Complex transaction descriptions might need manual categorization
- **Multi-Currency Handling**: Conversion rates need external data source or manual configuration

### Medium-Risk Areas
- **Manual Process Dependency**: Multiple page exports per month increases user effort
- **Test Data Limitations**: Anonymized test data may not cover all real-world format variations
- **Error Handling**: Graceful degradation for partial parsing failures

### Mitigation Strategies
- **Robust Regex**: Use flexible patterns with optional groups
- **Configuration**: Externalize regex patterns and account mappings
- **Logging**: Comprehensive audit trail for debugging
- **Fallback Mechanisms**: Manual review for unrecognized transactions

## Test Strategy

### Unit Tests
- **Regex Pattern Validation**: Test pattern matching with various input formats
- **Account Mapping Logic**: Verify category-to-account transformations
- **Date Parsing**: Validate date format conversions
- **Amount Extraction**: Test currency and amount parsing accuracy

### Integration Tests
- **End-to-End Workflow**: Complete text-to-ODS conversion pipeline
- **Multi-File Processing**: Test monthly statement processing with multiple input files
- **Error Scenarios**: Invalid input handling and error reporting

### Test Data Requirements
- **Real Format Samples**: Anonymized but representative input formats
- **Edge Cases**: Unusual transaction types, missing data, format variations
- **Multi-Currency Examples**: Test foreign currency transaction handling
- **Performance Data**: Typical and large file processing scenarios

## Implementation Hints

### Core Libraries
- **Text Processing**: Python `re` module for regex operations
- **ODS Generation**: `odfpy` library for OpenOffice file creation
- **Date Handling**: `datetime` module for date parsing and formatting
- **File Operations**: `pathlib` for robust file handling

### Development Priorities
1. **Core Parser**: Basic regex-based transaction extraction
2. **Account Mapping**: Category recognition and account code assignment
3. **ODS Generation**: Basic spreadsheet creation with required columns
4. **Multi-File Support**: Batch processing for monthly statements
5. **Error Handling**: Robust error reporting and logging
6. **CLI Interface**: User-friendly command-line interface

### Performance Considerations
- **Regex Compilation**: Pre-compile patterns for reuse
- **Memory Management**: Process files incrementally for large datasets
- **Caching**: Cache compiled patterns and mappings
- **Parallel Processing**: Consider threading for multiple file processing

### Code Organization
```
src/
├── parser/
│   ├── text_parser.py      # Regex-based text parsing
│   └── transaction.py      # Transaction data models
├── mapping/
│   ├── account_mapper.py   # Category-to-account mapping
│   └── config.py          # Configuration management
├── output/
│   └── ods_generator.py   # OpenOffice file generation
└── cli/
    └── main.py            # Command-line interface
```