# Test Strategy: Honeycomb + Component Focus

```text
         E2E (CLI workflows) - 5%
    🍯 Integration (Pipeline Tests) 🍯 - 60%  ← main focus
       Component (Parser/Mapper/ODS) - 25%
    🍯 Integration (Data Flow) 🍯
         Unit (Regex/Amounts) - 10%
```

- **Integration Focus (60%)**: Data pipeline testing is primary concern
- **Component Testing (25%)**: Isolated testing of Parser, Mapper, ODS Generator
- **Minimal Unit Testing (10%)**: Only for complex algorithms (regex, parsing)
- **Critical E2E Testing (5%)**: Complete CLI workflows with real data

## Test-Driven Development Approach

- **Write tests first**: Define expected behavior before implementation
- **Red-Green-Refactor**: Write failing test → implement feature → refactor code
- **Continuous testing**: Run tests after every change
- **Test coverage**: Aim for >90% code coverage from Phase 1

## Iterative Development

- Start with minimum viable implementation
- Add features incrementally  
- Test thoroughly at each stage
- Validate with real data early

## Key Success Factors

- **Robust parsing**: Handle format variations gracefully
- **Flexible configuration**: Easy to extend and modify
- **Clear error messages**: Help users resolve issues quickly
- **Test coverage**: Comprehensive testing from day one
