# Requirements Documentation

This directory contains the structured requirements documentation for the oneCreditCard project.

## Document Overview

- **[01-project-overview.md](01-project-overview.md)** - Project purpose, goals, and basic requirements
- **[02-input-format.md](02-input-format.md)** - Viseca text export format specification and parsing requirements
- **[03-output-format.md](03-output-format.md)** - ODS accounting format specification with column structure and account mapping
- **[04-technical-implementation.md](04-technical-implementation.md)** - Technical concept, risks, test scenarios, and implementation hints

## Quick Reference

**Project Purpose**: Convert credit card text exports from Viseca web portal to OpenOffice Calc accounting spreadsheets

**Input**: Unstructured text files from browser "Save as Text" exports
**Output**: ODS files with standardized accounting journal entries

**Key Technologies**: Python 3, regex parsing, odfpy library