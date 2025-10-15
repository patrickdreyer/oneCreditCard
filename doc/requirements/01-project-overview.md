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
- Support batch processing of multiple text export files
- Provide data validation and error reporting

## Open Questions

- What validation rules should be applied to extracted data?
- How should multi-currency transactions be handled (CHF/EUR conversions)?
- What specific account mapping rules should be applied for different transaction categories?

## Success Criteria

- Successfully parse all transaction data from Viseca text exports
- Generate properly formatted ODS files matching accounting requirements
- Handle multi-currency transactions correctly
- Process multiple files per monthly statement
- Provide clear error messages for invalid or incomplete data