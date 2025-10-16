# Architecture

## Processing Pipeline

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

## Parameter Default Behavior

- **No Parameters**: Process last month's data in current directory with default config
- **Month Detection**: Automatically determine previous month from current date
- **Config Discovery**: Look for configuration file in data folder with standard name
