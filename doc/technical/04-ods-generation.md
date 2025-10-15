# ODS Generation Implementation

## OpenOffice Calc File Generation

### Configurable ODS Structure

#### Dynamic Column Creation

The ODS file structure is defined by configuration file rather than hardcoded:

```python
def create_ods_from_config(transactions, config):
    """Create ODS file based on configuration structure"""
    doc = OpenDocumentSpreadsheet()
    table = Table(name="Transactions")
    
    # Create header row from configuration
    header_row = TableRow()
    columns = config['output_format']['columns']
    
    for column_config in columns:
        cell = TableCell()
        cell.addElement(P(text=column_config['name']))
        header_row.addElement(cell)
    
    table.addElement(header_row)
    return doc, table, columns
```

#### Configuration-Based Data Mapping

```python
def map_transaction_to_row(transaction, columns, account_mapping):
    """Map transaction data to ODS row based on configuration"""
    row = TableRow()
    
    for column_config in columns:
        cell = TableCell()
        value = get_column_value(transaction, column_config, account_mapping)
        cell.addElement(P(text=value))
        row.addElement(cell)
    
    return row

def get_column_value(transaction, column_config, account_mapping):
    """Get value for specific column based on configuration"""
    
    # Handle optional columns (no type field)
    if 'type' not in column_config:
        # Check if it's an always_empty column
        if column_config.get('always_empty', False):
            return ""
        # Default empty for optional columns without type
        return ""
    
    # Handle core columns (have type field)
    column_type = column_config['type']
    
    if column_type == 'date':
        return format_date(transaction.date, column_config.get('format', 'DD.MM.YY'))
    elif column_type == 'description':
        return get_description_from_mapping(transaction.category, account_mapping)
    elif column_type == 'debit_account':
        return get_debit_account(transaction.category, account_mapping)
    elif column_type == 'credit_account':
        return get_credit_account(transaction.category, account_mapping)
    elif column_type == 'amount_chf':
        return str(transaction.amount_chf)
    elif column_type == 'remarks':
        return get_remarks(transaction)
    else:
        return ""  # Default for unknown types
```

### Data Transformation

#### Transaction to Row Conversion

```python
def transaction_to_row(transaction):
    """Convert transaction object to ODS table row"""
    row = TableRow()
    
    # Date formatting (DD.MM.YYYY -> DD.MM.YY)
    date_cell = TableCell()
    formatted_date = format_date_short(transaction.date)
    date_cell.addElement(P(text=formatted_date))
    row.addElement(date_cell)
    
    # Description mapping
    desc_cell = TableCell()
    description = map_category_to_description(transaction.category)
    desc_cell.addElement(P(text=description))
    row.addElement(desc_cell)
    
    # Account codes
    debit_account, credit_account = get_account_codes(transaction.category)
    
    # Amount handling
    amount_cell = TableCell()
    amount_cell.addElement(P(text=str(transaction.amount_chf)))
    row.addElement(amount_cell)
    
    return row
```

### Account Code Mapping

#### Configuration-Based Mapping

Account mapping is loaded from configuration file at runtime:

```python
def load_account_mapping(config_path):
    """Load account mapping from configuration file"""
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config['account_mapping']

def get_account_codes(category, account_mapping):
    """Get debit and credit account codes for category"""
    mapping = account_mapping.get(category, {})
    return mapping.get('debit'), mapping.get('credit')

# Usage example
account_mapping = load_account_mapping('config.json')
debit_account, credit_account = get_account_codes('essen_trinken', account_mapping)
```

#### Configuration File Structure

```json
{
  "output_format": {
    "target_application": "banana",
    "columns": [
      {"name": "Datum", "type": "date", "format": "DD.MM.YY"},
      {"name": "Beschreibung", "type": "description"},
      {"name": "KtSoll", "type": "debit_account"},
      {"name": "KtHaben", "type": "credit_account"},
      {"name": "Betrag CHF", "type": "amount_chf", "format": "decimal"},
      {"name": "Bemerkungen", "type": "remarks"},
      {"name": "Saldo", "always_empty": true},
      {"name": "KS1", "always_empty": true},
      {"name": "KS2", "always_empty": true},
      {"name": "KS3", "always_empty": true}
    ]
  },
  "account_mapping": {
    "essen_trinken": {
      "description": "Verpflegung",
      "debit": "5821",
      "credit": "2110"
    }
  }
}
```

**Column Types:**

- **Core columns**: Have both `name` and `type` fields
- **Optional columns**: Have only `name` field, no `type`

### Configuration Rules

- **Core Columns**: Have `type` field, contain transaction data
- **Optional Columns**: No `type` field, used for compatibility/formatting
- **always_empty**: Optional columns that remain empty but maintain structure

### Multi-Currency Handling

#### Currency Conversion Strategy

```python
def handle_multi_currency(transaction):
    """Handle multi-currency transactions"""
    if transaction.foreign_currency and transaction.foreign_amount:
        # Store CHF amount in main column
        chf_amount = transaction.amount_chf
        
        # Store original currency in remarks
        remarks = f"{transaction.foreign_currency} {transaction.foreign_amount}"
        
        return chf_amount, remarks
    else:
        return transaction.amount_chf, ""
```

### File Operations

#### File Creation and Saving

```python
def create_ods_file(transactions, output_path):
    """Create ODS file from transaction list"""
    doc = OpenDocumentSpreadsheet()
    table = Table(name="Transactions")
    
    # Add header
    add_header_row(table)
    
    # Add transaction rows
    for transaction in transactions:
        row = transaction_to_row(transaction)
        table.addElement(row)
    
    doc.spreadsheet.addElement(table)
    doc.save(output_path)
```

#### File Naming Convention

```python
def generate_filename(transactions):
    """Generate filename from transaction dates"""
    dates = [t.date for t in transactions]
    year_month = min(dates).strftime("%Y-%m")
    return f"{year_month}.ods"
```

### Data Validation

#### Pre-Generation Validation

- **Required Fields**: Ensure date, amount, and category are present
- **Data Types**: Validate numeric amounts and date formats
- **Account Mapping**: Verify all categories have corresponding account codes
- **Currency Consistency**: Check currency handling for multi-currency transactions

#### Post-Generation Validation

- **File Integrity**: Verify ODS file can be opened
- **Data Accuracy**: Spot-check generated data against source
- **Format Compliance**: Ensure column structure matches requirements

### Error Handling

#### Generation Errors

- **Missing Data**: Handle transactions with incomplete information
- **Invalid Amounts**: Process malformed currency amounts
- **File Write Errors**: Handle disk space and permission issues
- **Library Errors**: Graceful handling of odfpy exceptions

### Performance Optimization

#### Memory Management

- **Streaming**: Process large transaction sets incrementally
- **Batch Processing**: Group transactions for efficient processing
- **Resource Cleanup**: Proper disposal of ODS document objects

#### Output Optimization

- **File Size**: Minimize generated file size
- **Compression**: Leverage ODS compression features
- **Formatting**: Optimize cell formatting for performance