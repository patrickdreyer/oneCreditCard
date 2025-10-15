# oneCreditCard - Requirements Document

## Overview

This document provides a high-level overview of the oneCreditCard project requirements. For detailed specifications, please refer to the structured documentation in the `doc/requirements/` directory.

## Project Purpose

Convert credit card text exports from Viseca web portal to OpenOffice Calc accounting spreadsheets for CFO workflows.

## Quick Summary

**Input**: Unstructured text files from browser "Save as Text" exports of Viseca web portal pages
**Output**: ODS files with standardized accounting journal entries
**Technology**: Python 3 with regex parsing and odfpy library

## Documentation Structure

📁 **[doc/requirements/](doc/requirements/README.md)** - Complete requirements documentation
- **[01-project-overview.md](doc/requirements/01-project-overview.md)** - Project goals, requirements, and success criteria
- **[02-input-format.md](doc/requirements/02-input-format.md)** - Viseca text export format and parsing patterns
- **[03-output-format.md](doc/requirements/03-output-format.md)** - ODS accounting format and account mapping rules
- **[04-technical-implementation.md](doc/requirements/04-technical-implementation.md)** - Architecture, risks, testing, and implementation guidance

## Key Requirements

- Parse unstructured Viseca web portal text exports
- Extract transaction data: date, amount, merchant, category, location
- Map transactions to accounting codes based on category
- Generate ODS files with specific column structure
- Handle multi-currency transactions (CHF/EUR)
- Support batch processing of monthly statement files
- Provide data validation and error reporting

## Next Steps

1. Review detailed requirements in `doc/requirements/` directory
2. Set up development environment with Python 3 and required dependencies
3. Implement core parsing and ODS generation functionality
4. Test with provided anonymized sample data in `tests/integration/testData/`