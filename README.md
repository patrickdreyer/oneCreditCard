# oneCreditCard

A Python tool that processes Viseca credit card text exports and converts them into accounting-ready OpenOffice Calc spreadsheets.

**Input**: Unstructured text files exported from Viseca/Migros Cumulus credit card web portal  
**Output**: Standardized accounting spreadsheets in OpenOffice Calc format  

## Quick Start

### Installation

#### System-Wide

```bash
sudo cp dist/onecreditcard /usr/local/bin/
onecreditcard --help
```

#### User-Local

```bash
mkdir -p ~/.local/bin
cp dist/onecreditcard ~/.local/bin/
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
onecreditcard --help
```

### Basic Usage

```bash
# Process credit card exports in current directory
python src/main.py

# Specify custom data folder and month
python src/main.py --folder /path/to/exports --month 2025-07

# Use custom configuration file
python src/main.py --config custom-config.json

# Enable debug logging
python src/main.py --log-level DEBUG

# Write logs to custom file
python src/main.py --log-file /var/log/onecreditcard.log
```

### Parameters

- **--folder, -f**: Data folder path (default: current working directory)
  - Contains input text files
  - Output ODS file will be created here
- **--month, -m**: Processing month in YYYY-MM format (default: previous month)
  - Filters transactions to specified month only
  - Used for output filename generation
- **--config, -c**: Configuration file path (default: {folder}/onecreditcard.json)
  - Contains account mapping rules and transaction categorization
  - Defines output format: column names, positions, and data formats
  - Processing settings and preferences
  - JSON format (see [Configuration Format](doc/technical/03-configuration-format.md))
- **--log-level**: Logging level (default: INFO)
  - Choices: DEBUG, INFO, WARNING, ERROR
  - Controls verbosity of console and log file output
- **--log-file**: Log file path (default: onecreditcard.log in current directory)
  - File where detailed logs are written
  - Console always shows INFO and above

## Features

- **Automated Text Parsing**: Extracts transaction data from unstructured Viseca web portal exports
- **Account Mapping**: Maps transaction categories to configurable accounting descriptions and codes
- **Multi-Currency Support**: Handles CHF and foreign currency transactions
- **Flexible Output**: Configurable OpenOffice Calc format for direct integration with accounting software
- **Batch Processing**: Process multiple text files representing monthly statements
- **Data Validation**: Ensures total amounts match between input and output

## Typical Workflow

1. **Export**: Download monthly statement as text from Viseca web portal (one file per page)
2. **Configure**: Set up account mapping in JSON configuration file
3. **Process**: Run python src/main.py to parse and convert data
4. **Import**: Load generated ODS file into accounting software (e.g., Banana Accounting)

## Documentation Structure

📁 **[doc/requirements/](doc/requirements/README.md)** - Business requirements

- **[Input Format](doc/requirements/01-input-format.md)** - Viseca text export structure  
- **[Output Format](doc/requirements/02-output-format.md)** - OpenOffice Calc file structure and format requirements
- **[Transaction Processing](doc/requirements/03-transaction-processing.md)** - Business logic for filtering, grouping, mapping, and processing transactions

📁 **[doc/technical/](doc/technical/README.md)** - Technical implementation

- **[Architecture](doc/technical/01-architecture.md)** - System overview and CLI parameters
- **[Account Mapping](doc/technical/02-account-mapping.md)** - Category to account code mapping
- **[Configuration Format](doc/technical/03-configuration-format.md)** - Configuration format comparison and decision
- **[Test Strategy](doc/technical/04-test-strategy.md)** - Honeycomb + Component testing approach and implementation
- **[Code Organization](doc/technical/05-code-organization.md)** - Project structure, modules, and file organization

📁 **[doc/development/](doc/development/README.md)** - Development guidance

- **[Implementation Guide](doc/development/01-implementation-guide.md)** - Development phases and testing strategy
- **[Parsing Implementation](doc/development/02-parsing-implementation.md)** - Text parsing patterns and regex implementation
- **[ODS Generation](doc/development/03-ods-generation.md)** - OpenOffice Calc file generation technical details

## AI Collaboration

📄 **[ai.md](ai.md)** - AI Context Document for team collaboration

- **Purpose**: Provides complete project context for AI-assisted development sessions
- **Usage**: Team members can run "load ai.md" to give AI full project understanding
- **Content**: Project overview, development environment strategy, multi-platform setup, collaboration guidelines
- **Team Context**: Cross-platform development (Ubuntu + Mac + Windows) with DevContainer strategy

## License

[License information to be added]

**Owner**: patrickdreyer
