# oneCreditCard

Credit card expense processing tool for CFO workflows - converts Viseca text exports to accounting spreadsheets.

## Overview

**Purpose**: Convert credit card text exports from Viseca web portal to OpenOffice Calc accounting spreadsheets  
**Target User**: CFO and accounting staff  
**Input**: Browser-saved text files from Viseca credit card portal  
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

# Process specific month
onecreditcard --month 2025-07

# Use custom configuration
onecreditcard --config my-config.json
```

### Input Parameters

- **Data Folder**: Path to folder with text files and output location (default: current directory)
- **Month**: Processing month in YYYY-MM format (default: last month)  
- **Configuration**: Path to account mapping configuration file (default: data folder)

## Features

- **Automated Processing**: Convert multiple text files per monthly statement
- **Category Mapping**: Automatically categorize expenses (food, transport, etc.)
- **Multi-Currency Support**: Handle CHF and EUR transactions
- **Configurable Output**: Flexible accounting format configuration
- **Ignore Rules**: Skip payments and unwanted transactions
- **Error Reporting**: Clear feedback on processing issues

## Contributing

1. **Setup Environment**: Follow [development setup guide](doc/development/02-development-setup.md)
2. **Review Implementation Plan**: Study [implementation guide](doc/development/01-implementation-guide.md)
3. **Understand Architecture**: Review technical documentation in `doc/technical/`
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

## Contact

**Repository**: [oneCreditCard](https://github.com/patrickdreyer/oneCreditCard)  
**Owner**: patrickdreyer