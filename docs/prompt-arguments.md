# Prompt Arguments

When running the `cookiecutter` command, an interactive prompt will ask you to configure the project. All parameters:

| Parameter | Default | Description |
| ----------- | --------- | ------------- |
| **plugin_id** | `obsidian-plugin` | Plugin identifier and folder name. Used in `manifest.json` and the generated directory name. |
| **plugin_name** | `Obsidian Plugin` | Human-readable plugin name shown in Obsidian. |
| **author_name** | `Your Name` | Your full name. |
| **description** | `A minimal Obsidian plugin` | Short description for the manifest and package metadata. |
| **min_obsidian_version** | `1.5.0` | Minimum supported Obsidian version (format X.Y.Z). |
| **license** | `MIT` | License: MIT, Apache-2.0, BSD-3-Clause, GPL-3.0, ISC, or none. |
| **repo_url** | `https://github.com/yourname/obsidian-plugin` | Repository URL (must be GitHub HTTPS). |
| **node_version** | `20` | Node.js version in CI (major version, e.g. 20). |
| **enable_vitest** | `no` | `yes` — add Vitest and example tests; `no` — no tests. |
| **enable_i18n** | `no` | `yes` — add locales and i18n helper; `no` — no i18n. |
