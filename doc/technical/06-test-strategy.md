# Test Strategy

## Test Architecture: Honeycomb + Component Focus

This document outlines the test strategy for the oneCreditCard project, emphasizing integration testing and component-based validation.

## Strategy Overview

### Test Distribution Model
```
         E2E (CLI workflows) - 5%
    🍯 Integration (Pipeline Tests) 🍯 - 60%  ← Hauptfokus
       Component (Parser/Mapper/ODS) - 25%
    🍯 Integration (Data Flow) 🍯
         Unit (Regex/Amounts) - 10%
```

**Rationale**: oneCreditCard is a **data pipeline application** where component integration is more critical than isolated unit functionality.

## Test Strategy Details

### 1. Integration Tests (60% - Primary Focus)

**Pipeline Integration Tests**
```python
def test_text_to_ods_complete_pipeline():
    """Test: Raw Viseca text → parsed transactions → mapped accounts → ODS file"""
    input_files = ['2025-07_1.txt', '2025-07_2.txt']
    config = load_test_config()
    
    result = process_month(input_files, config)
    
    assert result.ods_file.exists()
    assert result.total_amount == expected_total
    assert result.transaction_count == expected_count

def test_multi_file_aggregation():
    """Test: Multiple text files → consolidated monthly output"""
    
def test_configuration_integration():
    """Test: JSON config → category mapping → account assignment"""
    
def test_ignore_rules_integration():
    """Test: Ignore rules applied across complete workflow"""
```

**Data Flow Integration Tests**
```python
def test_amount_preservation_across_pipeline():
    """Verify: Sum of input amounts = Sum of output amounts"""
    
def test_currency_handling_integration():
    """Test: CHF amounts + EUR remarks handling"""
    
def test_error_propagation_integration():
    """Test: Error handling across component boundaries"""
```

### 2. Component Tests (25%)

**Isolated Component Testing**
```python
def test_parser_component_isolation():
    """Test parser with mocked file system and known input patterns"""
    
def test_mapper_component_isolation():
    """Test account mapping with various configuration scenarios"""
    
def test_ods_generator_component_isolation():
    """Test ODS generation with controlled transaction data"""
```

**Component Contract Testing**
```python
def test_parser_output_contract():
    """Ensure parser always returns valid Transaction objects"""
    
def test_mapper_input_contract():
    """Ensure mapper handles all valid Transaction variations"""
    
def test_ods_generator_input_contract():
    """Ensure ODS generator processes all mapped transaction formats"""
```

### 3. Unit Tests (10% - Minimal but Focused)

**Critical Algorithm Testing**
```python
def test_amount_extraction_regex():
    """Test complex regex patterns for amount extraction"""
    
def test_date_parsing_edge_cases():
    """Test date format variations and edge cases"""
    
def test_category_matching_algorithms():
    """Test flexible category matching logic"""
```

**Utility Function Testing**
```python
def test_file_pattern_recognition():
    """Test month-based file pattern matching"""
    
def test_data_validation_utilities():
    """Test data integrity validation functions"""
```

### 4. End-to-End Tests (5% - Critical Workflows Only)

**Complete CLI Workflows**
```python
def test_complete_cli_default_parameters():
    """Test: python main.py (with defaults)"""
    
def test_complete_cli_custom_config():
    """Test: python main.py --config custom.json --month 2025-07"""
    
def test_complete_cli_error_scenarios():
    """Test: CLI error handling and user feedback"""
```

## Test Implementation Strategy

### Phase 1: Foundation Tests
1. **Component Contracts**: Define and test interfaces between components
2. **Core Integration**: Basic pipeline functionality
3. **Critical Units**: Amount extraction and validation

### Phase 2: Pipeline Tests
1. **Multi-file Integration**: Batch processing workflows
2. **Configuration Integration**: Various config scenarios
3. **Error Handling Integration**: Graceful failure across components

### Phase 3: Production Readiness
1. **E2E CLI Testing**: Complete user workflows
2. **Performance Integration**: Large dataset processing
3. **Regression Testing**: Maintain existing functionality

## Testing Tools and Setup

### Primary Testing Stack
```python
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --cov=src --cov-report=html --cov-report=term-missing

# Test markers
markers =
    unit: Unit tests for isolated functions
    component: Component tests for isolated modules
    integration: Integration tests for component interaction
    e2e: End-to-end tests for complete workflows
    performance: Performance and load tests
```

### Test Data Strategy

For complete project structure including test organization, see:
**[Code Organization](07-code-organization.md)** - Project structure and file organization

**Test Directory Structure:**
- **tests/unit/**: Unit test files
- **tests/component/**: Component test files  
- **tests/integration/**: Integration test files
- **tests/e2e/**: End-to-end test files
- **tests/fixtures/**: Test data and configuration files

### Test Execution Strategy
```bash
# Development workflow
pytest tests/unit tests/component -x     # Fast feedback loop
pytest tests/integration                 # Integration validation
pytest tests/e2e                        # Full workflow validation

# CI Pipeline
pytest --cov=src --cov-fail-under=90    # Coverage enforcement
pytest tests/performance                # Performance regression
```

## Quality Gates

### Component Quality Gates
- **Parser**: Must handle all test data files without crashes
- **Mapper**: Must correctly map all known categories
- **ODS Generator**: Must produce valid OpenOffice files

### Integration Quality Gates  
- **Amount Integrity**: Input totals must equal output totals (±0.01 CHF)
- **Data Completeness**: All transactions must be processed (mapped or unmapped)
- **Configuration Flexibility**: Must handle various config scenarios

### Performance Quality Gates
- **Processing Speed**: <5 seconds for typical monthly data (NFR-01)
- **Memory Usage**: <100MB for standard datasets
- **File Size**: Output files <10MB for typical monthly data

## Test Maintenance

### Continuous Improvement
- **Regular review** of test effectiveness and coverage
- **Addition of new test cases** based on production issues
- **Refactoring of test code** to maintain clarity and speed
- **Update of test data** to reflect Viseca format changes

### Test Data Management
- **Anonymized real data** for realistic testing scenarios
- **Synthetic edge cases** for boundary condition testing
- **Version control** of test expectations and golden masters
- **Regular updates** to maintain relevance with actual usage patterns