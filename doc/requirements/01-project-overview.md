# Project Overview

This document outlines the user requirements and project goals for the oneCreditCard tool.

## User Story

As a small business owner using Viseca/Migros Cumulus credit cards, I want to efficiently convert monthly credit card statements into accounting-ready spreadsheets for import into my accounting software (Banana Accounting).

## Problem Statement

**Current Process (Manual):**

1. Download monthly statement as text files from Viseca web portal (one file per page)
2. Manually extract transaction data (date, amount, merchant, category)
3. Manually map transactions to accounting categories and codes
4. Manually create OpenOffice Calc spreadsheet with proper format
5. Import into accounting software

**Problems:**

- Time-consuming manual data entry
- Error-prone manual mapping
- Inconsistent formatting
- Repetitive monthly task

## Solution Overview

**Automated Process:**

1. Export monthly statement as text from Viseca web portal (unchanged)
2. Run onecreditcard tool on exported text files
3. Tool automatically parses, maps, and formats data
4. Import generated ODS file directly into accounting software

## Input Parameters

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
- **Month**: Filters transactions to specified month (transactions span multiple months)
- **Configuration**: JSON file defining category mapping to accounting codes and output format

## Success Criteria

- Successfully parse all transaction data from Viseca text exports
- Generate properly formatted ODS files with configurable accounting format
- Handle multi-currency transactions: All amounts in CHF with foreign currency in remarks
- Process multiple files per monthly statement  
- Validate total amounts: Sum of CHF amounts in input files equals sum in output ODS file
- Provide clear error messages for invalid or incomplete data
