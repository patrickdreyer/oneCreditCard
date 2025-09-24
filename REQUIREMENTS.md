# oneCreditCard - Requirements Document

## PDF Credit Card Export Processing

In order to streamline accounting processes and reduce manual data entry errors
As a CFO
I want to upload credit card expense PDFs and automatically generate OpenOffice Calc spreadsheets with properly formatted accounting bookings

### Open Questions
- Which PDF formats are supported (bank-specific layouts, scanned vs digital)?
- What specific accounting booking format is required?
- Should the tool handle multiple credit cards/accounts simultaneously?
- What validation rules should be applied to extracted data?

### Details
- Accept PDF files as input via command-line arguments or file paths
- Extract transaction data: date, amount, merchant, category, card number
- Generate OpenOffice Calc (.ods) files with accounting journal entries
- Include debit/credit columns, account codes, descriptions, and reference numbers
- Support batch processing of multiple PDF files
- Provide data validation and error reporting

### Concept
- PDF parsing using text extraction libraries (PyPDF2/pdfplumber)
- Transaction data extraction with regex patterns or ML-based parsing
- OpenOffice Calc file generation using python-odf library
- Command-line interface for file processing
- Configuration for accounting chart of accounts mapping

### Risks
- PDF format variations between different banks may require custom parsers
- OCR accuracy for scanned PDFs may be inconsistent
- Complex transaction descriptions might need manual categorization
- Large PDF files could impact processing performance

### Test Scenarios
- Unit tests for PDF text extraction accuracy
- Integration tests for complete PDF-to-spreadsheet workflow
- E2E tests with real bank statement PDFs
- Error handling tests for corrupted or unsupported PDF formats
- Performance tests with large batch processing

### Implementation Hints
- Use pdfplumber for robust PDF text extraction
- Consider pytesseract for OCR on scanned PDFs  
- Use odfpy or python-odf for OpenOffice Calc file generation
- Implement configurable regex patterns for different bank formats
- Add logging for audit trail of processing steps