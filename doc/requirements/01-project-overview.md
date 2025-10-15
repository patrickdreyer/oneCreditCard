# Project Overview

## Text Credit Card Export Processing

In order to streamline accounting processes and reduce manual data entry errors
As a CFO
I want to upload credit card expense text exports and automatically generate OpenOffice Calc spreadsheets with properly formatted accounting bookings

## Project Goals

- **Primary Goal**: Automate conversion of Viseca credit card exports to accounting format
- **Target User**: CFO and accounting staff
- **Input Source**: Browser-saved text files from Viseca web portal
- **Output Target**: OpenOffice Calc (.ods) files with journal entries

## Key Requirements

- Accept unstructured text export files from credit card web portals (Viseca format)
- Handle browser "Save as Text" exports from web portal pages
- Process monthly statements split across multiple text files (one per page)
- Parse transaction data using regex patterns: date, amount, merchant, category, location
- Extract transaction details embedded within web page text exports
- Generate OpenOffice Calc (.ods) files with specific accounting format
- Handle multi-currency transactions: CHF as base currency, foreign currencies in remarks column
- Support batch processing of multiple text export files
- Validate data integrity: Total CHF amounts from all input files must equal the sum in generated ODS file
- Provide data validation and error reporting

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

### Parameter Usage
- **Data Folder**: Contains input text files and receives output ODS file
- **Month Filter**: Only process transactions from the specified month
- **Configuration**: Defines account mapping rules, output format (column names/structure), transaction categorization, and processing settings

## Success Criteria

- Successfully parse all transaction data from Viseca text exports
- Generate properly formatted ODS files with configurable accounting format
- Handle multi-currency transactions: All amounts in CHF with foreign currency in remarks
- Process multiple files per monthly statement
- Validate total amounts: Sum of CHF amounts in input files equals sum in output ODS file
- Provide clear error messages for invalid or incomplete data