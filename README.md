# oneCreditCard

A Python tool that processes Viseca credit card text exports and converts them into accounting-ready OpenOffice Calc spreadsheets.

**Input**: Unstructured text files exported from Viseca/Migros Cumulus credit card web portal  
**Output**: Standardized accounting spreadsheets in OpenOffice Calc format  

## Quick Start

### Installation

```bash
git clone https://github.com/patrickdreyer/oneCreditCard.git
cd oneCreditCard
pip install -r requirements.txt
```

### Basic Usage

```bash
# Process credit card exports in current directory
onecreditcard

# Specify custom data folder and month
onecreditcard --data-folder /path/to/exports --month 2025-07

# Use custom configuration file
onecreditcard --config custom-config.json
```

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
3. **Process**: Run onecreditcard to parse and convert data
4. **Import**: Load generated ODS file into accounting software (e.g., Banana Accounting)

## Getting Started

1. **Read Documentation**: Start with [project overview](doc/requirements/01-project-overview.md)
2. **Review Sample Data**: Check examples in `tests/fixtures/inputs/`
3. **Understand Format**: Study [input](doc/requirements/02-input-format.md) and [output](doc/requirements/03-output-format.md) formats
4. **Examine Test Data**: Analyze samples in `tests/fixtures/inputs/`
5. **Begin Implementation**: Start with Phase 1 priorities (Core Parser → Account Mapping → ODS Generation)

## Documentation Structure

📁 **[doc/requirements/](doc/requirements/README.md)** - Business requirements and user needs

- **[Project Overview](doc/requirements/01-project-overview.md)** - Project goals and user requirements
- **[Input Format](doc/requirements/02-input-format.md)** - Input data format from user perspective  
- **[Output Format](doc/requirements/03-output-format.md)** - Required accounting output format
- **[Formal Requirements](doc/requirements/04-formal-requirements.md)** - Formal functional and non-functional requirements

📁 **[doc/technical/](doc/technical/README.md)** - Technical implementation details

- **[System Architecture](doc/technical/01-architecture.md)** - System architecture and design
- **[Account Mapping](doc/technical/02-account-mapping.md)** - Transaction mapping and configuration
- **[Parsing Implementation](doc/technical/03-parsing-implementation.md)** - Text parsing technical details
- **[ODS Generation](doc/technical/04-ods-generation.md)** - Spreadsheet generation implementation
- **[Configuration Format](doc/technical/05-configuration-format.md)** - Configuration format comparison
- **[Test Strategy](doc/technical/06-test-strategy.md)** - Honeycomb + Component testing approach

📁 **[doc/development/](doc/development/README.md)** - Development guidance and setup

- **[Implementation Guide](doc/development/01-implementation-guide.md)** - Development priorities and phases
- **[Development Setup](doc/development/02-development-setup.md)** - Environment setup and tools
- **[Performance Guidelines](doc/development/03-performance-guidelines.md)** - Performance considerations

## AI Collaboration

📄 **[ai.md](ai.md)** - AI Context Document for team collaboration

- **Purpose**: Provides complete project context for AI-assisted development sessions
- **Usage**: Team members can run "load ai.md" to give AI full project understanding
- **Content**: Project overview, development environment strategy, multi-platform setup, collaboration guidelines
- **Team Context**: Cross-platform development (Ubuntu + Mac + Windows) with DevContainer strategy

## License

[License information to be added]

**Owner**: patrickdreyer
