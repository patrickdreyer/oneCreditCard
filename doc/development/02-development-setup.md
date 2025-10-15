# Development Setup

## Environment Requirements

### Python Version
- **Required**: Python 3.13 or higher
- **Recommended**: Python 3.13+ for best performance and features

### Operating System
- **Cross-Platform**: Ubuntu (Linux), macOS, and Windows
- **Development Environment**: VS Code Dev Containers with Podman
- **Shell**: bash (recommended on Linux/Mac), PowerShell or Git Bash (Windows)

## Multi-Platform Development Strategy

**Decision**: Use VS Code Dev Containers with Podman for consistent cross-platform development.

**Benefits:**
- Identical development environment across Ubuntu, Mac, and Windows
- Isolation from system Python installations  
- Reproducible setup for all team members
- Modern container-based development workflow

**Setup Overview:**
- **Container Engine**: Podman (instead of Docker)
- **Development**: VS Code with Dev Containers extension
- **Base Environment**: Python 3.13 with all project dependencies
- **Implementation**: To be set up collaboratively with team member

## Dependencies

**Note**: When using Dev Containers, dependencies are automatically installed in the container environment.

### Core Dependencies
```bash
pip install -r requirements.txt
```

### Development Dependencies
```bash
pip install pytest pytest-cov black flake8 mypy
```

**Key Packages:**
- **odfpy**: OpenOffice Calc file generation
- **pytest**: Testing framework

## Development Tools

### Code Quality
- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking
- **pytest**: Testing

### VS Code Setup
- **Dev Containers extension**: For container-based development
- **Python extension**: Language support and debugging
- **Podman extension**: Container management integration
- **GitHub Copilot**: AI assistance (recommended)
- **Auto-install**: Project includes `.vscode/extensions.json` for automatic extension recommendations

Configure formatters and linters in container environment

### Git Configuration
```bash
git config --local user.name "Your Name"
git config --local user.email "your.email@example.com"
```

## File Structure Setup

### Test Data
Test data and configuration files are organized as follows:
```bash
# Sample input files (to be moved to fixtures)
ls tests/fixtures/inputs/
# Expected: 2025-07_1.txt, 2025-07_2.txt, etc.

# Test configuration files
ls tests/fixtures/configs/
# Expected: test-config.json, edge-case-config.json, etc.
```

### Configuration
Create sample configuration:
```bash
mkdir -p config
cp doc/technical/02-account-mapping.md config/example-config.json
# Edit the JSON examples to create actual config file
```

## Development Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Development Cycle
```bash
# Make changes
# Run tests
python -m pytest tests/

# Format code
black src/ tests/

# Check linting
flake8 src/ tests/

# Type checking
mypy src/
```

### 3. Commit Changes
```bash
git add .
git commit -m "descriptive commit message"
```

### 4. Push and Pull Request
```bash
git push origin feature/your-feature-name
# Create pull request via GitHub
```

## Testing Setup

**Quick Testing Commands:**
```bash
# Run all tests
pytest

# Run with coverage  
pytest --cov=src tests/

# Run specific test categories
pytest tests/integration/  # Integration tests
pytest tests/unit/         # Unit tests
```

## Troubleshooting

### Common Issues

**ModuleNotFoundError**:
```bash
# Ensure PYTHONPATH includes src directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

**Permission Errors**:
```bash
# Check file permissions
chmod +x scripts/*.py
```

**Test Failures**:
```bash
# Run tests in verbose mode
pytest -v --tb=short
```

### Dependencies Issues
```bash
# Update pip
pip install --upgrade pip

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### IDE Configuration Issues
- Ensure Python interpreter points to virtual environment
- Configure code formatter (Black) and linter (Flake8)
- Set up debugging configuration for pytest

## Performance Monitoring

### Profiling Setup
```bash
# Install profiling tools
pip install memory-profiler line-profiler
```

### Memory Monitoring
```bash
# Monitor memory usage during development
python -m memory_profiler src/main.py
```

### Benchmarking
```bash
# Run performance benchmarks
pytest tests/performance/ --benchmark-only
```

## Next Steps

1. **Verify Setup**: Run all tests successfully
2. **Create First Feature**: Start with core parser implementation
3. **Follow Implementation Guide**: Use development priorities from `01-implementation-guide.md`
4. **Regular Testing**: Run tests frequently during development

For implementation guidance, see [Implementation Guide](01-implementation-guide.md).