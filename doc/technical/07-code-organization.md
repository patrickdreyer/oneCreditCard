# Code Organization

## Project Structure

```
oneCreditCard/
├── .git/
├── .gitignore
├── README.md
├── requirements.txt          # Python dependencies
├── doc/
│   ├── requirements/         # Business requirements
│   ├── technical/            # Technical specifications  
│   └── development/          # Development documentation
├── src/
│   ├── parser/
│   │   ├── textParser.py     # Regex-based text parsing
│   │   └── transaction.py    # Transaction data models
│   ├── mapping/
│   │   ├── accountMapper.py  # Category-to-account mapping
│   │   └── config.py         # Configuration management
│   ├── output/
│   │   └── odsGenerator.py   # OpenOffice file generation
│   └── cli/
│       └── main.py           # Command-line interface
├── tests/
│   ├── unit/                 # Unit test files
│   │   ├── test_parser.py
│   │   ├── test_mapping.py
│   │   └── test_output.py
│   ├── component/            # Component test files
│   │   ├── test_parser_component.py
│   │   └── test_mapper_component.py
│   ├── integration/          # Integration test files
│   │   └── test_workflow.py
│   ├── e2e/                  # End-to-end test files
│   │   └── test_cli_workflows.py
│   ├── fixtures/             # Test data and fixtures
│   │   ├── configs/          # Test configuration files
│   │   ├── inputs/           # Sample Viseca text files (anonymized)
│   │   └── expected/         # Expected ODS outputs
│   └── conftest.py           # pytest configuration
└── config/
    └── example-config.json   # Sample configuration
```

## Module Responsibilities

### Parser Module (`src/parser/`)
- **textParser.py**: Main parsing logic
  - File reading and preprocessing
  - Regex pattern matching
  - Transaction extraction
  - Data validation

- **transaction.py**: Data models
  - Transaction class definition
  - Data validation methods
  - Serialization/deserialization

### Mapping Module (`src/mapping/`)
- **accountMapper.py**: Category mapping logic
  - Category matching (flexible)
  - Account code assignment
  - Ignore rule processing
  - Grouping and summation

- **config.py**: Configuration management
  - JSON configuration loading
  - Validation of configuration structure
  - Default value handling

### Output Module (`src/output/`)
- **odsGenerator.py**: ODS file generation
  - Spreadsheet creation using odfpy
  - Column configuration handling
  - Data formatting
  - File output management

### CLI Module (`src/cli/`)
- **main.py**: Command-line interface
  - Argument parsing
  - Workflow orchestration
  - Error handling and reporting
  - Progress display

## Key Design Principles

### Separation of Concerns
- Each module has a single, well-defined responsibility
- Minimal coupling between modules
- Clear interfaces and contracts

### Configuration-Driven
- Parsing patterns externalized where possible
- Account mapping fully configurable
- Output format customizable
- Easy to extend without code changes

### Error Resilience
- Graceful handling of malformed input
- Clear error messages with context
- Partial processing when possible
- Comprehensive logging

### Testability
- Small, focused functions
- Dependency injection for external resources
- Mock-friendly interfaces
- Comprehensive test coverage

## Development Guidelines

### Code Style
- Follow PEP 8 style guidelines
- Use type hints where beneficial
- Comprehensive docstrings
- Meaningful variable and function names

### Documentation
- Module-level docstrings explaining purpose
- Function docstrings with parameters and return values
- Inline comments for complex logic
- README files for major components

### Testing Strategy
- Unit tests for individual functions
- Integration tests for module interactions
- End-to-end tests for complete workflows
- Performance tests for large datasets