import js from "@eslint/js";
import tseslint from "typescript-eslint";
import obsidianmd from "eslint-plugin-obsidianmd";
import globals from "globals";

export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.recommended,
  ...obsidianmd.configs.recommended,
  {
    files: ["src/**/*.ts", "tests/**/*.ts"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        ...globals.browser,
      },
      parserOptions: {
        projectService: {
          allowDefaultProject: [
            "eslint.config.js",
            "manifest.json",
            "versions.json"
          ]
        },
        tsconfigRootDir: import.meta.dirname,
        extraFileExtensions: [".json"]
      }
    }
  },
  {
    ignores: [
      "main.js",
      "node_modules/",
      "*.cjs",
      "*.config.js",
      "*.config.ts",
      "vitest.config.ts",
      "eslint.config.js",
      "esbuild.config.mjs",
      "version-bump.mjs"
    ]
  }
);
