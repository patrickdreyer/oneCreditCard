# Formal Requirements Specification

This document specifies the formal functional and non-functional requirements for the oneCreditCard project.

## Functional Requirements

### Input Processing

- **FR-01**: Accept unstructured text export files from Viseca credit card web portal
- **FR-02**: Handle browser "Save as Text" exports from web portal pages
- **FR-03**: Process monthly statements split across multiple text files (one per page)
- **FR-04**: Support batch processing of multiple text export files

### Data Extraction

- **FR-05**: Parse transaction data using regex patterns: date, amount, merchant, category, location
- **FR-06**: Extract transaction details embedded within web page text exports
- **FR-07**: Handle multi-currency transactions: CHF as base currency, foreign currencies in remarks column
- **FR-08**: Recognize and categorize transaction types (food, transport, shopping, etc.)

### Account Mapping

- **FR-09**: Map transaction categories to accounting descriptions and account codes
- **FR-10**: Group transactions with same accounting description and sum amounts
- **FR-11**: Handle unmapped transactions individually with empty debit account
- **FR-12**: Support ignore rules for categories and specific transactions

### Output Generation

- **FR-13**: Generate OpenOffice Calc (.ods) files with specific accounting format
- **FR-14**: Support configurable column structure and naming
- **FR-15**: Include all mapped and unmapped transactions in output
- **FR-16**: Preserve foreign currency information in remarks column

### Configuration

- **FR-17**: Accept JSON configuration files for account mapping and settings
- **FR-18**: Support flexible category matching (case-insensitive, whitespace-tolerant)
- **FR-19**: Allow configuration of output format: column names, positions, data formats

## Non-Functional Requirements

### Performance

- **NFR-01**: Process typical monthly statements (5-20 transactions) in under 5 seconds
- **NFR-02**: Handle large datasets (100+ transactions) efficiently
- **NFR-03**: Maintain low memory footprint during processing

### Usability

- **NFR-04**: Provide command-line interface with sensible defaults
- **NFR-05**: Generate clear error messages for invalid or incomplete data
- **NFR-06**: Support default parameter values (current directory, last month, default config)

### Reliability

- **NFR-07**: Validate data integrity: Sum of CHF amounts in input files equals sum in output ODS file
- **NFR-08**: Handle parsing errors gracefully without crashing
- **NFR-09**: Provide comprehensive error reporting and logging

### Maintainability

- **NFR-10**: Use configuration-driven approach for mapping rules and output format
- **NFR-11**: Support extensible category and account mapping
- **NFR-12**: Maintain clean separation between parsing, mapping, and output generation

## Input Parameters

The system must accept the following input parameters:

### Required Parameters

- **Data Folder Path**: Path to folder containing text files and where ODS file will be created
  - Default: Current working directory
- **Processing Month**: Month for which data should be extracted  
  - Format: YYYY-MM (e.g., "2025-07")
  - Default: Previous month from current date
- **Configuration File Path**: Path to configuration file for account mapping and settings
  - Default: Same folder as data files
  - Default filename: "onecreditcard.json"

## Success Criteria

- Successfully parse all transaction data from Viseca text exports
- Generate properly formatted ODS files with configurable accounting format
- Handle multi-currency transactions: All amounts in CHF with foreign currency in remarks
- Process multiple files per monthly statement
- Validate total amounts: Sum of CHF amounts in input files equals sum in output ODS file
- Provide clear error messages for invalid or incomplete data

## Dependencies

- Python 3.13+
- odfpy library for OpenOffice Calc file generation
- Standard Python libraries (re, json, datetime, pathlib)

## Constraints

- Input format depends on Viseca web portal layout (may change over time)
- No complex multi-currency scenarios (CHF + occasional foreign currency only)
- Monthly processing model (not real-time)
- Text-based input only (no PDF or other formats)

## Requirements Traceability

| Requirement ID | Implementation Status | Test Coverage | Notes |
|----------------|----------------------|---------------|-------|
| FR-01 to FR-04 | Not Started | - | Core parsing functionality |
| FR-05 to FR-08 | Not Started | - | Data extraction logic |
| FR-09 to FR-12 | Not Started | - | Account mapping system |
| FR-13 to FR-16 | Not Started | - | ODS output generation |
| FR-17 to FR-19 | Not Started | - | Configuration management |
| NFR-01 to NFR-03 | Not Started | - | Performance requirements |
| NFR-04 to NFR-06 | Not Started | - | Usability requirements |
| NFR-07 to NFR-09 | Not Started | - | Reliability requirements |
| NFR-10 to NFR-12 | Not Started | - | Maintainability requirements |

*Note: This traceability matrix should be updated during implementation to track progress and ensure all requirements are met.*
