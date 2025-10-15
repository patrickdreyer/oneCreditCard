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
# Run tests frequently
pytest tests/

# Format code
black src/ tests/

# Lint code  
flake8 src/ tests/

# Type check
mypy src/
```

### 3. Testing Strategy

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test categories
pytest tests/ -k "unit"
pytest tests/ -k "integration"
```

### 4. Code Quality Check

```bash
# Full quality check pipeline
black src/ tests/
flake8 src/ tests/
mypy src/
pytest tests/ --cov=src
```

### 5. Commit and Push

```bash
git add .
git commit -m "feat: descriptive commit message"
git push origin feature/your-feature-name
```

## Dev Container Setup (Ubuntu + Mac + Windows)

### Prerequisites

1. **VS Code**: Latest version with Dev Containers extension
2. **Podman**: Install Podman Desktop for your platform
3. **Git**: For version control

### Platform-Specific Podman Installation

#### Ubuntu/Linux

```bash
# Install Podman
sudo apt update
sudo apt install podman

# Enable Podman socket for VS Code integration
systemctl --user enable --now podman.socket
```

#### macOS

```bash
# Install Podman Desktop from: https://podman-desktop.io/
# Or via Homebrew:
brew install podman
podman machine init
podman machine start
```

#### Windows

```bash
# Install Podman Desktop from: https://podman-desktop.io/
# Or via winget:
winget install RedHat.Podman-Desktop
```

### VS Code Configuration

1. **Install Extensions:**
   - Dev Containers (ms-vscode-remote.remote-containers)
   - Python (ms-python.python)

2. **Configure Podman Path:**
   Add to VS Code settings.json:

```json
{
    "dev.containers.dockerPath": "podman"
}
```

### Project Setup

1. **Clone Repository:**

```bash
git clone https://github.com/patrickdreyer/oneCreditCard.git
cd oneCreditCard
```

1. **Open in Dev Container:**
   - Open VS Code in project directory
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Select "Dev Containers: Reopen in Container"
   - Wait for container build and setup

1. **Verify Setup:**

```bash
# Check Python version
python --version  # Should show Python 3.13.x

# Run tests
pytest tests/ -v

# Check installed packages
pip list
```

## Troubleshooting

### Common Issues

1. **Podman Socket Connection (Linux):**

```bash
# If VS Code can't connect to Podman
systemctl --user status podman.socket
systemctl --user restart podman.socket
```

1. **Permission Issues (Windows):**
   - Run Podman Desktop as Administrator
   - Ensure Windows Subsystem for Linux (WSL) is enabled

1. **Container Build Failures:**

```bash
# Clear Podman cache
podman system prune -a

# Rebuild container
# In VS Code: "Dev Containers: Rebuild Container"
```

### Performance Optimization

1. **Enable Podman Caching:**

```bash
# Add to ~/.config/containers/storage.conf
[storage.options]
mount_program = "/usr/bin/fuse-overlayfs"
```

1. **VS Code Settings for Better Performance:**

```json
{
    "python.analysis.autoImportCompletions": true,
    "python.analysis.autoSearchPaths": true,
    "files.watcherExclude": {
        "**/.git/objects/**": true,
        "**/node_modules/**": true,
        "**/__pycache__/**": true
    }
}
```

## Next Steps

1. **Complete Dev Container setup** following this guide
2. **Run initial tests** to verify environment
3. **Review project documentation** in `doc/` directory
4. **Start development** following the coding guidelines
5. **Set up git hooks** for automated quality checks (optional)
