# AI Context Document - oneCreditCard Project

## Project Overview
- **Project Name**: oneCreditCard (repository: oneCreditCard)
- **Purpose**: Credit card expense processing tool - Viseca text exports → OpenOffice Calc accounting spreadsheets
- **Owner**: patrickdreyer
- **Current Branch**: main
- **Team**: Ubuntu (Patrick) + Mac (Alexandra)

## Development Environment Strategy
- **Container Engine**: Podman (instead of Docker)
- **Development Platform**: VS Code Dev Containers
- **Cross-Platform Solution**: Ubuntu + Mac + Windows compatibility via containers
- **Base Environment**: Python 3.13 with project dependencies

## Multi-Platform Collaboration Context
### Current Development Setup Decision
- **Decision Made**: Use VS Code Dev Containers with Podman for consistent cross-platform development
- **Implementation Status**: Documented in doc/development/02-development-setup.md
- **Next Steps**: Alexandra will implement DevContainer setup with AI assistance

### Alexandra DevContainer Implementation Tasks
When Alexandra collaborates with AI, she will implement:
1. **Podman Desktop Setup** for Mac
2. **VS Code Dev Containers Extension** installation
3. **.devcontainer/devcontainer.json** configuration creation
4. **Podman integration** with VS Code settings
5. **Development workflow** testing and validation

### DevContainer Technical Specifications
- **Base Image**: python:3.13-bookworm
- **Key Dependencies**: odfpy, pytest, black, flake8, mypy, ruff
- **VS Code Configuration**: Python formatter, linter, testing setup
- **Container Path**: `"dev.containers.dockerPath": "podman"`

## Documentation Status
### Requirements & Architecture: ✅ Complete
- Business requirements fully documented in doc/requirements/
- Technical architecture specified in doc/technical/
- Test strategy (Honeycomb + Component Focus) implemented
- Implementation guidelines ready

## AI Behavior Rules
1. **Context Loading**: When user writes "load ai.md", read this file AND all documentation in doc/ directory
1. **Development Context**: Reference complete documentation structure for project details
1. **Collaboration Support**: Provide hands-on technical assistance for DevContainer setup to Alexandra
- **Cross-Platform Awareness**: Consider Ubuntu + Mac + Windows compatibility in all recommendations
1. **Container-First Approach**: Assume Podman + Dev Containers as primary development environment
1. **Context Updates**: Proactively propose updates to ai.md when new information or changes are relevant
1. **No Context Proposals**: Never provide proposed changes for ai.md context itself - update directly
1. **Code Proposals**: Show diffs/descriptions only, not full code blocks unless explicitly requested
1. **Confirmation Required**: Any changes within the project must be confirmed by the user before execution
1. **Short & Concise**: Keep responses brief and to the point. No unnecessary explanations.
1. **English Only**: All responses and artifacts must be in English, regardless of chat language used
1. **No Assumptions**: Always ask for approval before:
   - Creating new files or directories
   - Modifying existing code
   - Installing dependencies
   - Running commands that could affect the project
   - Any other modifications to the workspace

## Development Guidelines
- Source code goes in `src/`
- Tests go in `tests/`
- Documentation in `doc/` (requirements/ and technical/)
- Follow user's explicit instructions and preferences
- Reference structured documentation for complete project context

## Configuration
- OS: Linux
- Shell: bash
- IDE: VS Code

## Notes
- Complete project details are in doc/requirements/ and doc/technical/
- AI should always reference full documentation context
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
