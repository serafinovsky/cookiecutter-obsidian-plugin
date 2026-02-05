from pathlib import Path

from helpers import (
    assert_file_contains,
    assert_file_exists,
    assert_file_not_exists,
    cleanup_project,
    get_default_context,
    get_template_dir,
    run_cookiecutter,
)


class TestBasicGeneration:
    def test_basic_project_generation(self):
        """Test that a basic project is generated correctly."""
        template_dir = get_template_dir()
        context = get_default_context()

        project_path = run_cookiecutter(template_dir, context)

        try:
            # Check that essential files exist
            assert_file_exists(project_path, "manifest.json")
            assert_file_exists(project_path, "package.json")
            assert_file_exists(project_path, "README.md")
            assert_file_exists(project_path, "LICENSE")
            assert_file_exists(project_path, "src/main.ts")
            assert_file_exists(project_path, "styles.css")
            assert_file_exists(project_path, "versions.json")
            assert_file_exists(project_path, "tsconfig.json")
            assert_file_exists(project_path, "Makefile")

            # Check manifest.json content
            assert_file_contains(project_path, "manifest.json", '"id": "test-plugin"')
            assert_file_contains(project_path, "manifest.json", '"name": "Test Plugin"')
            assert_file_contains(project_path, "manifest.json", '"description": "A test plugin"')
            assert_file_contains(project_path, "manifest.json", '"minAppVersion": "1.5.0"')

            # Check package.json content
            assert_file_contains(project_path, "package.json", '"name": "test-plugin"')
            assert_file_contains(project_path, "package.json", '"description": "A test plugin"')

            # Check README.md content
            assert_file_contains(project_path, "README.md", "# Test Plugin")
            assert_file_contains(project_path, "README.md", "A test plugin")

            # Check LICENSE content
            assert_file_contains(project_path, "LICENSE", "MIT License")
            assert_file_contains(project_path, "LICENSE", "Test Author")
        finally:
            cleanup_project(project_path)

    def test_project_with_vitest(self):
        """Test project generation with Vitest enabled."""
        template_dir = get_template_dir()
        context = get_default_context()
        context["enable_vitest"] = "yes"
        project_path = run_cookiecutter(template_dir, context)
        try:
            assert_file_exists(project_path, "vitest.config.ts")
            assert_file_exists(project_path, "tests/smoke.test.ts")
            assert_file_contains(project_path, "package.json", '"test": "vitest run"')
        finally:
            cleanup_project(project_path)

    def test_project_without_vitest(self):
        """Test project generation without Vitest."""
        template_dir = get_template_dir()
        context = get_default_context()
        context["enable_vitest"] = "no"
        project_path = run_cookiecutter(template_dir, context)
        try:
            assert_file_not_exists(project_path, "vitest.config.ts")
            assert_file_not_exists(project_path, "tests")
        finally:
            cleanup_project(project_path)

    def test_project_with_i18n(self):
        """Test project generation with i18n enabled."""
        template_dir = get_template_dir()
        context = get_default_context()
        context["enable_i18n"] = "yes"
        project_path = run_cookiecutter(template_dir, context)
        try:
            assert_file_exists(project_path, "locales/en.json")
            assert_file_exists(project_path, "src/i18n/index.ts")
        finally:
            cleanup_project(project_path)

    def test_project_without_i18n(self):
        """Test project generation without i18n."""
        template_dir = get_template_dir()
        context = get_default_context()
        context["enable_i18n"] = "no"
        project_path = run_cookiecutter(template_dir, context)
        try:
            assert_file_not_exists(project_path, "locales")
            assert_file_not_exists(project_path, "src/i18n")
        finally:
            cleanup_project(project_path)

    def test_plugin_id_generation(self):
        """Test that plugin id is used for folder name."""
        template_dir = get_template_dir()
        context = get_default_context()
        context["plugin_id"] = "my-awesome-plugin"
        project_path = run_cookiecutter(template_dir, context)
        try:
            assert Path(project_path).name == "my-awesome-plugin"
            assert_file_contains(project_path, "manifest.json", '"id": "my-awesome-plugin"')
        finally:
            cleanup_project(project_path)
