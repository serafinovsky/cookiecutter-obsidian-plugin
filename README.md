# Obsidian Plugin Template

![Logo](docs/assets/logo.png)

![License](https://img.shields.io/badge/license-MIT-green)
![Cookiecutter](https://img.shields.io/badge/cookiecutter-template-red)
[![Tests passed](https://github.com/serafinovsky/cookiecutter-obsidian-plugin/workflows/Checks/badge.svg)](https://github.com/serafinovsky/cookiecutter-obsidian-plugin/actions)
![Tox](https://img.shields.io/badge/tox-multi--version-blue)
![Pytest](https://img.shields.io/badge/pytest-testing-blue)
![Ruff](https://img.shields.io/badge/ruff-linting-blue)
[![Documentation](https://img.shields.io/badge/docs-latest-blue)](https://serafinovsky.github.io/cookiecutter-obsidian-plugin)

**Cookiecutter template for creating Obsidian plugins with a ready-to-use structure and tooling.**

## Quick Start

### Using cookiecutter directly

```bash
# Install cookiecutter
pip install cookiecutter

# Create project
cookiecutter https://github.com/serafinovsky/cookiecutter-obsidian-plugin -o your-obsidain-vault/.obsidian/plugins/

# Setup plugin development environment
cd your-plugin-id
make install
make dev 
```

### Using CLI tool

```bash
# Install the CLI tool
pip install cookiecutter-obsidian-plugin

# Or with custom options
cookiecutter-obsidian-plugin --output-dir your-obsidain-vault/.obsidian/plugins/

# Setup plugin development environment
cd your-plugin-id
make install
make dev 
```

## Key Features

### Modern Tools

TypeScript, ESLint, esbuild, and optional Vitest and i18n setup

### CI/CD Ready

GitHub Actions with ready-to-use release workflow for plugins.

[CI/CD](features/ci-cd.md) · [Release Workflow](features/release-workflow.md)

### Code Quality

ESLint (linter), Prettier (formatter), and optional tests — all configured automatically

## Documentation

Documentation is available here: [Docs](https://serafinovsky.github.io/cookiecutter-obsidian-plugin/)

## License

MIT License
