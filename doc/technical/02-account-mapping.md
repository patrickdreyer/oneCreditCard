# Account Mapping Implementation

## Purpose

Technical implementation of category-to-account mapping from JSON configuration.

## Configuration Structure

```json
{
  "creditAccount": "2110",
  "ignore": {
    "categories": ["Einlagen"],
    "transactions": ["Ihre Zahlung - Danke"]
  },
  "mapping": {
    "Essen & Trinken": {
      "description": "Verpflegung",
      "debitAccount": "5821"
    }
  },
  "columns": [
    {"name": "Datum", "type": "date", "format": "DD.MM.YY"},
    {"name": "Beschreibung", "type": "description"},
    {"name": "KtSoll", "type": "debitAccount"},
    {"name": "KtHaben", "type": "creditAccount"},
    {"name": "Betrag CHF", "type": "amountChf", "format": "decimal"},
    {"name": "Saldo"},
    {"name": "KS1"},
    {"name": "KS2"},
    {"name": "KS3"},
    {"name": "Bemerkungen", "type": "remarks"}
  ]
}
```

## Column Configuration Rules

- **Core Columns**: Have `type` field, contain actual transaction data
- **Optional Columns**: No `type` field, used for formatting/compatibility (remain empty)

## Implementation Details

### Configuration Loading

```python
def load_account_mapping(config_path):
    """Load account mapping from JSON configuration"""
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config

def get_account_codes(category, account_mapping):
    """Get debit and credit account codes for category"""
    mapping = account_mapping.get('mapping', {}).get(category, {})
    debit = mapping.get('debitAccount', '')
    credit = account_mapping.get('creditAccount', '2110')
    return debit, credit
```

### Flexible Category Matching

```python
def normalize_category(category):
    """Normalize category for flexible matching"""
    return re.sub(r'\s+', ' ', category.strip().lower())

def find_matching_category(input_category, config_mapping):
    """Find matching category with flexible matching"""
    normalized_input = normalize_category(input_category)
    
    for config_key in config_mapping.keys():
        if normalize_category(config_key) == normalized_input:
            return config_key
    return None
```

### Error Handling

```python
def validate_configuration(config):
    """Validate configuration structure"""
    required_fields = ['creditAccount', 'mapping', 'columns']
    for field in required_fields:
        if field not in config:
            raise ConfigurationError(f"Missing required field: {field}")
    
    # Validate account codes format
    for category, mapping in config['mapping'].items():
        if 'debitAccount' not in mapping:
            raise ConfigurationError(f"Missing debitAccount for {category}")
```
