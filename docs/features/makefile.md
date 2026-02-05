# Makefile

Commands from your plugin `Makefile`:

| Command | Purpose |
| --- | --- |
| `make install` | Install dependencies |
| `make build` | Build the plugin |
| `make dev` | Build in watch mode |
| `make lint` | Run ESLint |
| `make lint-fix` | Fix ESLint issues |
| `make format` | Run Prettier |
| `make format-check` | Check formatting |
| `make check` | ESLint + Prettier check |
| `make test` | Run tests (if Vitest enabled) |
| `make coverage` | Coverage report (if Vitest enabled) |
| `make patch` | `0.1.2` → `0.1.3` |
| `make minor` | `0.1.2` → `0.2.0` |
| `make major` | `0.1.2` → `1.0.0` |
| `make release` | Push commits and tags |
| `make tags` | List git tags |
