import tempfile
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner
from helpers import (
    assert_file_contains,
    assert_file_exists,
    assert_file_not_exists,
    cleanup_project,
)

from cookiecutter_obsidian_plugin.cli import get_template_dir, main


class TestGetTemplateDir:
    """Test the get_template_dir function."""

    def test_get_template_dir_returns_correct_path(self):
        """Test that get_template_dir returns the correct template directory path."""
        template_dir = get_template_dir()

        # Should point to the project root directory
        assert_file_exists(template_dir, "/")
        assert_file_exists(template_dir, "cookiecutter.json")
        assert_file_exists(template_dir, "{{cookiecutter.plugin_id}}")


class TestCLIMain:
    """Test the main CLI function."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_help_command(self):
        """Test that the help command works correctly."""
        result = self.runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert "Create a new Obsidian plugin using a cookiecutter template" in result.output
        assert "--output-dir" in result.output
        assert "--no-input" in result.output
        assert "--replay" in result.output
        assert "--overwrite-if-exists" in result.output
        assert "--skip-if-file-exists" in result.output
        assert "--config-file" in result.output

    def test_version_command(self):
        """Test that the version command works correctly."""
        result = self.runner.invoke(main, ["--version"])

        assert result.exit_code == 0
        assert "version" in result.output.lower()

    @patch("cookiecutter_obsidian_plugin.cli.cookiecutter")
    def test_basic_project_creation(self, mock_cookiecutter):
        """Test basic project creation with default options."""
        with tempfile.TemporaryDirectory() as mock_project_dir:
            mock_cookiecutter.return_value = mock_project_dir

        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.runner.invoke(main, ["--output-dir", temp_dir, "--no-input"])

            assert result.exit_code == 0
            assert "Creating new Obsidian plugin..." in result.output
            assert "Project successfully created at:" in result.output
            assert "Next steps:" in result.output

            # Verify cookiecutter was called with correct arguments
            mock_cookiecutter.assert_called_once()
            call_args = mock_cookiecutter.call_args

            assert call_args[1]["output_dir"] == temp_dir
            assert call_args[1]["no_input"] is True
            assert call_args[1]["replay"] is False
            assert call_args[1]["overwrite_if_exists"] is False
            assert call_args[1]["skip_if_file_exists"] is False
            assert call_args[1]["config_file"] is None

    @patch("cookiecutter_obsidian_plugin.cli.cookiecutter")
    def test_project_creation_with_all_flags(self, mock_cookiecutter):
        """Test project creation with all CLI flags enabled."""
        with tempfile.TemporaryDirectory() as temp_dir, tempfile.TemporaryDirectory() as mock_project_dir:
            mock_cookiecutter.return_value = mock_project_dir
            config_file = Path(temp_dir) / "config.yaml"
            config_file.write_text("test: config")

            result = self.runner.invoke(
                main,
                [
                    "--output-dir",
                    temp_dir,
                    "--no-input",
                    "--replay",
                    "--overwrite-if-exists",
                    "--skip-if-file-exists",
                    "--config-file",
                    str(config_file),
                ],
            )

            assert result.exit_code == 0

            # Verify cookiecutter was called with correct arguments
            mock_cookiecutter.assert_called_once()
            call_args = mock_cookiecutter.call_args

            assert call_args[1]["output_dir"] == temp_dir
            assert call_args[1]["no_input"] is True
            assert call_args[1]["replay"] is True
            assert call_args[1]["overwrite_if_exists"] is True
            assert call_args[1]["skip_if_file_exists"] is True
            assert call_args[1]["config_file"] == str(config_file)

    @patch("cookiecutter_obsidian_plugin.cli.cookiecutter")
    def test_project_creation_with_short_flags(self, mock_cookiecutter):
        """Test project creation with short flags."""
        with tempfile.TemporaryDirectory() as temp_dir, tempfile.TemporaryDirectory() as mock_project_dir:
            mock_cookiecutter.return_value = mock_project_dir
            result = self.runner.invoke(
                main,
                [
                    "-o",
                    temp_dir,
                    "-f",  # --overwrite-if-exists
                    "-s",  # --skip-if-file-exists
                ],
            )

            assert result.exit_code == 0

            # Verify cookiecutter was called with correct arguments
            mock_cookiecutter.assert_called_once()
            call_args = mock_cookiecutter.call_args

            assert call_args[1]["output_dir"] == temp_dir
            assert call_args[1]["overwrite_if_exists"] is True
            assert call_args[1]["skip_if_file_exists"] is True

    @patch("cookiecutter_obsidian_plugin.cli.cookiecutter")
    def test_cookiecutter_error_handling(self, mock_cookiecutter):
        """Test that cookiecutter errors are handled properly."""
        mock_cookiecutter.side_effect = Exception("Test error")

        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.runner.invoke(main, ["--output-dir", temp_dir, "--no-input"])

            assert result.exit_code == 1
            assert "Error creating project: Test error" in result.output

    def test_invalid_output_directory(self):
        """Test handling of invalid output directory."""
        result = self.runner.invoke(main, ["--output-dir", "/nonexistent/directory", "--no-input"])

        # Should fail with click's path validation error
        assert result.exit_code != 0
        assert "does not exist" in result.output.lower()

    def test_invalid_config_file(self):
        """Test handling of invalid config file."""
        result = self.runner.invoke(main, ["--config-file", "/nonexistent/config.yaml", "--no-input"])

        # Should fail with click's path validation error
        assert result.exit_code != 0
        assert "does not exist" in result.output.lower()

    @patch("cookiecutter_obsidian_plugin.cli.cookiecutter")
    def test_default_output_directory(self, mock_cookiecutter):
        """Test that default output directory is current working directory."""
        with tempfile.TemporaryDirectory() as mock_project_dir:
            mock_cookiecutter.return_value = mock_project_dir

            result = self.runner.invoke(main, ["--no-input"])

            assert result.exit_code == 0

            # Verify cookiecutter was called with current directory
            mock_cookiecutter.assert_called_once()
            call_args = mock_cookiecutter.call_args

            # The output_dir should be the string representation of current directory
            assert Path(call_args[1]["output_dir"]).exists()

    @patch("cookiecutter_obsidian_plugin.cli.cookiecutter")
    def test_template_directory_is_correct(self, mock_cookiecutter):
        """Test that the correct template directory is passed to cookiecutter."""
        with tempfile.TemporaryDirectory() as mock_project_dir:
            mock_cookiecutter.return_value = mock_project_dir

            result = self.runner.invoke(main, ["--no-input"])

            assert result.exit_code == 0

            # Verify cookiecutter was called with correct template directory
            mock_cookiecutter.assert_called_once()
            call_args = mock_cookiecutter.call_args

            template_dir = call_args[0][0]  # First positional argument
            template_path = Path(template_dir)

            assert template_path.exists()
            assert (template_path / "cookiecutter.json").exists()
            assert (template_path / "{{cookiecutter.plugin_id}}").exists()

    @patch("cookiecutter_obsidian_plugin.cli.cookiecutter")
    def test_output_messages(self, mock_cookiecutter):
        """Test that correct output messages are displayed."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_project_path = str(Path(temp_dir) / "my-test-project")
            mock_cookiecutter.return_value = test_project_path

            result = self.runner.invoke(main, ["--no-input"])

            assert result.exit_code == 0
            assert "Creating new Obsidian plugin..." in result.output
            assert f"Project successfully created at: {test_project_path}" in result.output
            assert "Next steps:" in result.output
            assert f"cd {Path.cwd() / 'my-test-project'}" in result.output
            assert "make install" in result.output
            assert "make build" in result.output
            assert "For detailed setup instructions, see the README.md file" in result.output


class TestCLIRealGeneration:
    """Test CLI with real project generation using helpers."""

    def setup_method(self):
        self.runner = CliRunner()

    def test_real_project_generation_with_defaults(self):
        """Test real project generation with default context."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.runner.invoke(main, ["--output-dir", temp_dir, "--no-input"])

            assert result.exit_code == 0
            assert "Creating new Obsidian plugin..." in result.output
            assert "Project successfully created at:" in result.output

            project_dirs = list(Path(temp_dir).glob("*"))
            assert len(project_dirs) == 1
            project_path = str(project_dirs[0])

            try:
                assert_file_exists(project_path, "manifest.json")
                assert_file_exists(project_path, "package.json")
                assert_file_exists(project_path, "README.md")
                assert_file_exists(project_path, "LICENSE")
                assert_file_exists(project_path, "src/main.ts")
                assert_file_exists(project_path, "styles.css")
                assert_file_exists(project_path, "versions.json")
                assert_file_exists(project_path, "tsconfig.json")
                assert_file_exists(project_path, "Makefile")

                assert_file_contains(project_path, "manifest.json", '"id": "obsidian-plugin"')
                assert_file_contains(project_path, "manifest.json", '"name": "Obsidian Plugin"')
                assert_file_contains(project_path, "manifest.json", '"minAppVersion": "1.5.0"')
                assert_file_contains(project_path, "manifest.json", '"description": "A minimal Obsidian plugin"')

                assert_file_contains(project_path, "package.json", '"name": "obsidian-plugin"')
                assert_file_contains(project_path, "package.json", '"description": "A minimal Obsidian plugin"')

                assert_file_contains(project_path, "README.md", "# Obsidian Plugin")
                assert_file_contains(project_path, "README.md", "A minimal Obsidian plugin")

                assert_file_contains(project_path, "LICENSE", "MIT License")
            finally:
                cleanup_project(project_path)

    def test_real_project_generation_with_custom_context(self):
        """Test real project generation with custom context via config file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "config.yml"
            config_file.write_text("""
default_context:
  plugin_id: "custom-plugin"
  plugin_name: "Custom Plugin"
  description: "Custom plugin description"
  enable_i18n: "yes"
""")

            result = self.runner.invoke(
                main, ["--output-dir", temp_dir, "--no-input", "--config-file", str(config_file)]
            )

            assert result.exit_code == 0

            project_dirs = list(Path(temp_dir).glob("*"))
            project_dirs = [p for p in project_dirs if p.is_dir()]
            assert len(project_dirs) == 1
            project_path = str(project_dirs[0])

            try:
                assert_file_exists(project_path, "manifest.json")
                assert_file_exists(project_path, "locales/en.json")
                assert_file_exists(project_path, "src/i18n/index.ts")

                assert_file_contains(project_path, "manifest.json", '"id": "custom-plugin"')
                assert_file_contains(project_path, "manifest.json", '"name": "Custom Plugin"')
                assert_file_contains(project_path, "manifest.json", '"description": "Custom plugin description"')
            finally:
                cleanup_project(project_path)

    def test_real_project_generation_with_vitest(self):
        """Test real project generation with Vitest enabled."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "config.yml"
            config_file.write_text("""
default_context:
  enable_vitest: "yes"
""")

            result = self.runner.invoke(
                main, ["--output-dir", temp_dir, "--no-input", "--config-file", str(config_file)]
            )

            assert result.exit_code == 0

            project_dirs = list(Path(temp_dir).glob("*"))
            project_dirs = [p for p in project_dirs if p.is_dir()]
            assert len(project_dirs) == 1
            project_path = str(project_dirs[0])

            try:
                assert_file_exists(project_path, "vitest.config.ts")
                assert_file_exists(project_path, "tests/smoke.test.ts")
                assert_file_contains(project_path, "package.json", '"test": "vitest run"')
            finally:
                cleanup_project(project_path)

    def test_real_project_generation_without_vitest(self):
        """Test real project generation without Vitest."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "config.yml"
            config_file.write_text("""
default_context:
  enable_vitest: "no"
""")

            result = self.runner.invoke(
                main, ["--output-dir", temp_dir, "--no-input", "--config-file", str(config_file)]
            )

            assert result.exit_code == 0

            project_dirs = list(Path(temp_dir).glob("*"))
            project_dirs = [p for p in project_dirs if p.is_dir()]
            assert len(project_dirs) == 1
            project_path = str(project_dirs[0])

            try:
                assert_file_not_exists(project_path, "vitest.config.ts")
                assert_file_not_exists(project_path, "tests")
            finally:
                cleanup_project(project_path)

    def test_real_project_generation_without_i18n(self):
        """Test real project generation without i18n."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "config.yml"
            config_file.write_text("""
default_context:
  enable_i18n: "no"
""")

            result = self.runner.invoke(
                main, ["--output-dir", temp_dir, "--no-input", "--config-file", str(config_file)]
            )

            assert result.exit_code == 0

            project_dirs = list(Path(temp_dir).glob("*"))
            project_dirs = [p for p in project_dirs if p.is_dir()]
            assert len(project_dirs) == 1
            project_path = str(project_dirs[0])

            try:
                assert_file_not_exists(project_path, "locales")
                assert_file_not_exists(project_path, "src/i18n")
            finally:
                cleanup_project(project_path)
