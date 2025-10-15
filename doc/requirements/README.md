# Requirements Documentation

This directory contains the business and user requirements for the oneCreditCard project.

## Quick Summary

**User Goal**: Convert credit card text exports to accounting spreadsheets
**Input**: Browser-saved text files from Viseca credit card portal  
**Output**: Standardized accounting spreadsheets in OpenOffice Calc format  
**Target User**: CFO and accounting staff  

## Key User Requirements

- **Simple Input**: Accept text files saved from browser
- **Automated Processing**: Convert multiple files per monthly statement  
- **Standard Output**: Generate accounting-ready spreadsheets
- **Category Mapping**: Automatically categorize expenses (food, transport, etc.)
- **Multi-Currency Support**: Handle CHF and EUR transactions
- **Error Reporting**: Clear feedback on processing issues

## Document Overview

- **[Project Overview](01-project-overview.md)** - Project purpose, goals, and user requirements
- **[Input Format](02-input-format.md)** - Viseca text export format from user perspective
- **[Output Format](03-output-format.md)** - Required accounting format and business rules
- **[Formal Requirements](04-formal-requirements.md)** - Formal functional and non-functional requirements specification
