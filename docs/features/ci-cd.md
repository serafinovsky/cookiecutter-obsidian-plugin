# CI/CD with GitHub Actions

## ci.yml

Triggers: push and PR to `main`/`master`.

1. `npm install`
2. `npm run check` (ESLint + Prettier)
3. `npm run test` (if Vitest enabled)
4. `npm run build`

## release.yml

Triggers: push tags matching `v*`.

1. `npm install`
2. `npm run test` (if Vitest enabled)
3. `npm run build`
4. Publishes release with `main.js`, `manifest.json`, `styles.css`

## Secrets

None required. Release uses default `contents: write` permission.
