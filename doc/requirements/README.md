# Requirements Documentation

## User Story

Convert monthly Viseca credit card statements from browser text exports into accounting-ready OpenOffice Calc spreadsheets.

## Key User Requirements

- **Simple Input**: Accept text files saved from browser
- **Automated Processing**: Convert multiple files per monthly statement  
- **Standard Output**: Generate accounting-ready spreadsheets
- **Category Mapping**: Automatically categorize expenses (food, transport, etc.)
- **Multi-Currency Support**: Handle CHF and EUR transactions
- **Error Reporting**: Clear feedback on processing issues

## Problem

**Current manual process:**

1. Export text files from Viseca web portal (multiple files per month)
1. Manually extract transaction data
1. Map to accounting categories
1. Create spreadsheet for accounting import

## Solution

**Automated process:**

1. Export text files (unchanged)
1. Run tool on exported files  
1. Import generated ODS directly into accounting software

## Documents

- **[Input Format](01-input-format.md)** - Viseca text export structure  
- **[Output Format](02-output-format.md)** - Accounting ODS requirements
