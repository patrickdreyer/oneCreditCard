# Configuration Format Comparison

This document compares different configuration formats to justify the choice for the oneCreditCard project.

## Recommendation: JSON

### Reasoning:
1. ✅ **Zero Dependencies**: No additional libraries required
2. ✅ **Universal Support**: Every developer knows JSON
3. ✅ **Excellent Tooling**: VS Code, validation, formatting built-in
4. ✅ **Simple Deployment**: Works out-of-the-box on any system
5. ✅ **Project Fit**: Our configuration is moderately complex but manageable in JSON

### Trade-offs Accepted:
- ❌ **No Comments**: Documentation will be in separate files (which is better practice anyway)
- ❌ **Strict Syntax**: Actually helps prevent configuration errors
- ❌ **Verbose**: Acceptable for the configuration size we expect

### Configuration File Specification:
- **Format**: JSON
- **Extension**: `.json`
- **Default Name**: `onecreditcard.json`
- **Location**: Same directory as input data files
- **Validation**: JSON Schema can be provided for validation

## Alternative for Future Consideration:
If the configuration becomes significantly more complex or user feedback indicates JSON is too difficult, **TOML** would be the next best choice due to its excellent readability and rich data type support.

## Decision Matrix

| Criteria | JSON | TOML | YAML | INI |
|----------|------|------|------|-----|
| **Simplicity** | 🟢 | 🟡 | 🔴 | 🟢 |
| **No Dependencies** | 🟢 | 🔴 | 🔴 | 🟢 |
| **Comments Support** | 🔴 | 🟢 | 🟢 | 🟢 |
| **User Friendly** | 🟡 | 🟢 | 🟢 | 🔴 |
| **Tooling Support** | 🟢 | 🟡 | 🟡 | 🟡 |
| **Error Tolerant** | 🟡 | 🟢 | 🔴 | 🟢 |

**Legend**: 🟢 Excellent | 🟡 Good | 🔴 Poor

## Format Comparison

### JSON (JavaScript Object Notation)
**Pros:**
- ✅ Wide language support (native Python support)
- ✅ Simple syntax, well-known
- ✅ No additional dependencies
- ✅ Good tooling support in IDEs
- ✅ Validation schemas available (JSON Schema)

**Cons:**
- ❌ No comments support
- ❌ Strict syntax (trailing commas not allowed)
- ❌ Limited data types (no dates, no multiline strings)

**Example:**
```json
{
  "mapping": {
    "Essen & Trinken": {
      "description": "Verpflegung",
      "debitAccount": "5821",
      "creditAccount": "2110"
    },
    "Fahrzeug": {
      "description": "Auto; Diesel",
      "debitAccount": "6210",
      "creditAccount": "2110"
    }
  },
  "columns": [
    {"name": "Datum", "type": "date", "format": "DD.MM.YY"},
    {"name": "Beschreibung", "type": "description"},
    {"name": "KtSoll", "type": "debitAccount"},
    {"name": "Betrag CHF", "type": "amountChf", "format": "decimal"}
  ]
}
```

### TOML (Tom's Obvious Minimal Language)
**Pros:**
- ✅ Human-readable and writable
- ✅ Comments support
- ✅ Rich data types (dates, arrays, nested objects)
- ✅ Less verbose than JSON for complex configurations
- ✅ No ambiguous syntax

**Cons:**
- ❌ Additional dependency required (`tomli`/`tomllib` in Python 3.13+)
- ❌ Less familiar to most developers
- ❌ More complex parsing

**Example:**
```toml
# Account mapping configuration for oneCreditCard

[mapping."Essen & Trinken"]
description = "Verpflegung"
debitAccount = "5821"
creditAccount = "2110"

[mapping."Fahrzeug"]
description = "Auto; Diesel"
debitAccount = "6210"
creditAccount = "2110"

[[columns]]
name = "Datum"
type = "date"
format = "DD.MM.YY"

[[columns]]
name = "Beschreibung"
type = "description"

[[columns]]
name = "KtSoll"
type = "debitAccount"

[[columns]]
name = "Betrag CHF"
type = "amountChf"
format = "decimal"
```

### YAML (YAML Ain't Markup Language)
**Pros:**
- ✅ Very human-readable
- ✅ Comments support
- ✅ Rich data types
- ✅ Multiline strings
- ✅ No brackets/braces needed

**Cons:**
- ❌ Indentation-sensitive (whitespace errors)
- ❌ Additional dependency required (`PyYAML`)
- ❌ Complex specification with edge cases
- ❌ Security concerns (arbitrary code execution)

**Example:**
```yaml
# Account mapping configuration
mapping:
  "Essen & Trinken":
    description: "Verpflegung"
    debitAccount: "5821"
    creditAccount: "2110"
  "Fahrzeug":
    description: "Auto; Diesel"
    debitAccount: "6210"
    creditAccount: "2110"

columns:
  - name: "Datum"
    type: "date"
    format: "DD.MM.YY"
  - name: "Beschreibung"
    type: "description"
  - name: "KtSoll"
    type: "debitAccount"
  - name: "Betrag CHF"
    type: "amountChf"
    format: "decimal"
```

### INI Format
**Pros:**
- ✅ Simple and familiar
- ✅ Comments support
- ✅ Built-in Python support (`configparser`)
- ✅ Good for simple configurations

**Cons:**
- ❌ Limited nesting capabilities
- ❌ No arrays/lists support
- ❌ Limited data types
- ❌ Not suitable for complex structures

**Example:**
```ini
# Simple configuration format - not suitable for complex mapping
[mapping_essen_trinken]
description = Verpflegung
debitAccount = 5821
creditAccount = 2110

[mapping_fahrzeug]
description = Auto; Diesel
debitAccount = 6210
creditAccount = 2110

# INI format cannot properly represent arrays, so columns would be:
[column_1]
name = Datum
type = date
format = DD.MM.YY

[column_2]
name = Beschreibung
type = description
```
