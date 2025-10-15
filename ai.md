# AI Context Document - oneCreditCard Project

## Project Overview
- **Project Name**: oneCreditCard (repository: oneCreditCart)
- **Purpose**: PDF credit card expense processing tool for CFO accounting workflows - converts credit card PDFs to OpenOffice Calc spreadsheets
- **Owner**: patrickdreyer
- **Current Branch**: main

## Technology Stack
- **Language**: Python 3
- **Framework**: [To be defined]
- **Database**: [To be defined]
- **Testing**: pytest

## Dependencies
- pytest (testing framework)
- pdfplumber (PDF text extraction)
- odfpy (OpenOffice Calc file generation)

## Coding Standards
- [To be defined based on language/framework choice]

## Project Structure
```
oneCreditCart/
├── .git/
├── .gitignore
├── REQUIREMENTS.md   # Project requirements and specifications
├── requirements.txt  # Python dependencies
├── src/
│   └── main.py       # Entry point - Hello World console app
├── tests/
│   └── test_main.py  # Unit tests for main.py
└── ai.md             # This context document
```

## AI Behavior Rules
1. **Context Loading**: When user writes "load ai.md", read this file to understand project context and rules
2. **Context Updates**: Proactively propose updates to ai.md when new information or changes are relevant
3. **No Context Proposals**: Never provide proposed changes for ai.md context itself - update directly
4. **Code Proposals**: Show diffs/descriptions only, not full code blocks unless explicitly requested
5. **Confirmation Required**: Any changes within the project must be confirmed by the user before execution
6. **Short & Concise**: Keep responses brief and to the point. No unnecessary explanations.
7. **English Only**: All responses and artifacts must be in English, regardless of chat language used
8. **No Assumptions**: Always ask for approval before:
   - Creating new files or directories
   - Modifying existing code
   - Installing dependencies
   - Running commands that could affect the project
   - Any other modifications to the workspace

## Development Guidelines
- Source code goes in `src/`
- Tests go in `tests/`
- Follow user's explicit instructions and preferences

## Session History
- **2024-09-24 Session 1**: 
  - Created initial project structure (src/, tests/)
  - Established confirmation-required workflow
  - Set up ai.md context document
  - Added behavior rules for concise responses
  - Created REQUIREMENTS.md with PDF-to-spreadsheet CFO workflow specs

## Project Goals
- [To be defined]

## Next Steps
- [To be updated as project evolves]

## Configuration
- OS: Linux
- Shell: bash
- IDE: VS Code

## Notes
- Project appears to be in early setup phase
- User prefers explicit control over all changes

# Requirement template
```markdown
In order to <why>
As <who>
I want to <what>

## Open Questions
- <Open questions for the development team regarding implementation.>

## Details
- <Specific, granular details of the technical implementation.>

## Concept
- <A brief overview of the technical approach or design.>

## Risks
- <Technical risks associated with this implementation (e.g., library limitations, performance).>

## Test Scenarios
- <Specific test cases (unit, integration, E2E) for this technical component.>

## Implementation hints
- <Suggestions for libraries, algorithms, or specific code patterns.>
```
