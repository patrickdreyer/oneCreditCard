# Technical Implementation Guide

## Architecture Concept

### Processing Pipeline
1. **Text File Input**: Read unstructured Viseca text exports
2. **Regex Parsing**: Extract transaction data using pattern matching
3. **Data Transformation**: Convert to accounting format with account mapping
4. **ODS Generation**: Create OpenOffice Calc files with specific structure
5. **Batch Processing**: Handle multiple input files for monthly statements

### Core Components
- **CLI Interface**: Command-line interface for file processing with parameter handling
- **Text Parser**: Regex-based extraction from unstructured web page text
- **Transaction Processor**: Data transformation and categorization logic
- **Account Mapper**: Category-to-account-code mapping from configuration
- **ODS Generator**: OpenOffice Calc file creation using odfpy
- **Configuration Manager**: Handle account mapping and processing settings

## Command Line Interface

### Input Parameters
```bash
# Example usage
onecreditcard --folder /path/to/data --month 2025-07 --config /path/to/config.json

# With defaults
onecreditcard  # Uses current directory, last month, default config
```

### Parameter Specification
- **--folder, -f**: Data folder path (default: current working directory)
  - Contains input text files
  - Output ODS file will be created here
- **--month, -m**: Processing month in YYYY-MM format (default: previous month)
  - Filters transactions to specified month only
  - Used for output filename generation
- **--config, -c**: Configuration file path (default: {data_folder}/onecreditcard.{ext})
  - Contains account mapping rules and transaction categorization
  - Defines output format: column names, positions, and data formats
  - Processing settings and preferences
  - JSON format (see [Configuration Format Comparison](05-configuration-format.md))

### Default Behavior
- **No Parameters**: Process last month's data in current directory with default config
- **Month Detection**: Automatically determine previous month from current date
- **Config Discovery**: Look for configuration file in data folder with standard name

## Implementation Strategy

### Text Parsing Approach
- **Regex Patterns**: Use compiled regex for performance
- **Multi-line Matching**: Handle transactions spanning multiple lines
- **Error Tolerance**: Graceful handling of parsing failures
- **Data Validation**: Verify extracted data completeness and format

### Account Mapping Logic
Account mapping and transaction grouping are core features of the system. Detailed configuration structure and mapping rules are documented in **[Account Mapping](02-account-mapping.md)**.

**Key Features:**
- **Transaction Grouping**: Group transactions by final accounting description and sum amounts
- **Merchant Overrides**: Priority mapping based on merchant name (e.g., SBB CFF FFS)
- **Category Mapping**: Map Viseca categories to accounting descriptions
- **Multi-Currency Support**: Preserve foreign currency info in remarks while summing CHF amounts

### Configuration Structure
The configuration uses a simplified flat structure:
- **mapping**: Direct category-to-account mapping (replaces nested categoryMapping)
- **columns**: Output column definitions with types and formatting

### Column Configuration Rules
- **Core Columns**: Have `type` field, contain actual transaction data
- **Optional Columns**: No `type` field, used for formatting/compatibility (remain empty)

**Simplified Configuration Example:**
```json
{
  "creditAccount": "2110",
  "ignore": {
    "categories": ["Einlagen"],
    "transactions": ["Ihre Zahlung - Danke"]
  },
  "mapping": {
    "Essen & Trinken": {
      "description": "Verpflegung",
      "debitAccount": "5821"
    }
  },
  "columns": [
    {"name": "Datum", "type": "date", "format": "DD.MM.YY"},
    {"name": "Beschreibung", "type": "description"},
    {"name": "KtSoll", "type": "debitAccount"},
    {"name": "KtHaben", "type": "creditAccount"},
    {"name": "Betrag CHF", "type": "amountChf", "format": "decimal"},
    {"name": "Saldo"},
    {"name": "KS1"},
    {"name": "KS2"},
    {"name": "KS3"},
    {"name": "Bemerkungen", "type": "remarks"}
  ]
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

For detailed implementation guidance, see **[Development Documentation](../development/README.md)**.