# Release Workflow

## Version bump

Use Makefile targets (run `check` first):

- `make patch` → `0.1.2` → `0.1.3`
- `make minor` → `0.1.2` → `0.2.0`
- `make major` → `0.1.2` → `1.0.0`

Version is updated automatically in `package.json`, `manifest.json`, `versions.json`, and a git tag is created.

## Release

```bash
make release
```

Pushes commits and tags. The tag triggers GitHub Actions.
