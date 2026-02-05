# After Install

Short guide for common next steps after you generate the project.

## First time developing plugins?

- Place the project under your vault at `.obsidian/plugins/your-plugin-id` for local testing.
- Run `make install` and `make dev` to build in watch mode.
- Edit `src/main.ts` (or new `.ts` files) and reload Obsidian to pick up changes.
- Enable the plugin in Obsidian settings.

## Releasing new releases

- If needed, update `minAppVersion` in `manifest.json`.
- Bump version with `make patch`, `make minor`, or `make major`.
  This updates `package.json`, `manifest.json`, `versions.json` and creates a `vX.Y.Z` tag.
- Run `make release` to push commits and tags.
  The tag triggers GitHub Actions to build and publish a release with `main.js`, `manifest.json`, `styles.css`.

## Adding your plugin to the community plugin list

- Follow the official docs: [docs.obsidian.md](https://docs.obsidian.md/)
- Publish an initial GitHub release.
- Open a PR in [obsidianmd/obsidian-releases](https://github.com/obsidianmd/obsidian-releases).

## Manually installing the plugin

Copy `main.js`, `manifest.json`, and `styles.css` to:
`VaultFolder/.obsidian/plugins/your-plugin-id/`

## i18n (optional)

- Enable `enable_i18n` during generation to include i18n scaffolding.
- Use `t()` from `src/i18n/index.ts` in your code.
- Add new locales under `locales/` (copy `locales/en.json` and register in `src/i18n/index.ts`).
- i18next docs: [i18next.com](https://www.i18next.com/)

## References

- Official docs: [docs.obsidian.md](https://docs.obsidian.md/)
- Obsidian sample plugin: [obsidianmd/obsidian-sample-plugin](https://github.com/obsidianmd/obsidian-sample-plugin)
