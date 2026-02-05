import tempfile
from pathlib import Path

import pytest
from helpers import get_template_dir, run_cookiecutter


class TestValidation:
    """Test input validation functionality."""

    @pytest.mark.parametrize(
        "invalid_plugin_id",
        [
            "123invalid",  # Starts with number
            "Plugin-Name",  # Uppercase
            "project@with#special$chars",  # Special characters
            "name_with_underscore",  # Underscore
            "",  # Empty
        ],
    )
    def test_invalid_plugin_id(self, invalid_plugin_id):
        """Test validation of invalid plugin ids."""
        template_dir = get_template_dir()

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                run_cookiecutter(template_dir, extra_context={"plugin_id": invalid_plugin_id}, output_dir=temp_dir)
                raise AssertionError(f"Expected validation error for plugin id: {invalid_plugin_id}")
            except RuntimeError as e:
                assert "Hook script failed" in str(e)

    @pytest.mark.parametrize(
        "invalid_version",
        [
            "1.5",  # Missing patch
            "1",  # Too short
            "v1.5.0",  # Prefix
            "1.5.0-beta",  # Pre-release
            "1.5.0.1",  # Too many segments
        ],
    )
    def test_invalid_min_obsidian_version(self, invalid_version):
        """Test validation of invalid min Obsidian versions."""
        template_dir = get_template_dir()

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                run_cookiecutter(
                    template_dir, extra_context={"min_obsidian_version": invalid_version}, output_dir=temp_dir
                )
                raise AssertionError(f"Expected validation error for min_obsidian_version: {invalid_version}")
            except RuntimeError as e:
                assert "Hook script failed" in str(e)

    @pytest.mark.parametrize(
        "valid_plugin_id",
        [
            "my-plugin",
            "my-awesome-plugin",
            "project123",
            "a",
            "my-plugin-123",
        ],
    )
    def test_valid_plugin_id(self, valid_plugin_id):
        """Test that valid plugin ids pass validation."""
        template_dir = get_template_dir()

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                project_path = run_cookiecutter(
                    template_dir, extra_context={"plugin_id": valid_plugin_id}, output_dir=temp_dir
                )
                assert Path(project_path).exists(), f"Failed for valid plugin id: {valid_plugin_id}"
            except RuntimeError as e:
                raise AssertionError(f"Unexpected error for valid plugin id '{valid_plugin_id}': {e}") from e

    @pytest.mark.parametrize(
        "valid_version",
        [
            "1.5.0",
            "0.16.3",
            "2.0.1",
        ],
    )
    def test_valid_min_obsidian_version(self, valid_version):
        """Test that valid min Obsidian versions pass validation."""
        template_dir = get_template_dir()

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                project_path = run_cookiecutter(
                    template_dir, extra_context={"min_obsidian_version": valid_version}, output_dir=temp_dir
                )
                assert Path(project_path).exists(), f"Failed for valid min_obsidian_version: {valid_version}"
            except RuntimeError as e:
                raise AssertionError(f"Unexpected error for valid min_obsidian_version '{valid_version}': {e}") from e

    @pytest.mark.parametrize(
        "invalid_url",
        [
            "http://github.com/user/repo",
            "https://gitlab.com/user/repo",
            "example.com/repo",
            "git@github.com:test/repo",
            "ftp://example.com/repo",
            "",
        ],
    )
    def test_invalid_repo_url(self, invalid_url):
        """Test validation of invalid repository URLs."""
        template_dir = get_template_dir()

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                run_cookiecutter(template_dir, extra_context={"repo_url": invalid_url}, output_dir=temp_dir)
                raise AssertionError(f"Expected validation error for repo_url: {invalid_url}")
            except RuntimeError as e:
                assert "Hook script failed" in str(e)

    @pytest.mark.parametrize(
        "valid_url",
        [
            "https://github.com/user/repo",
            "https://github.com/user/repo-name",
        ],
    )
    def test_valid_repo_url(self, valid_url):
        """Test validation of valid repository URLs."""
        template_dir = get_template_dir()

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                project_path = run_cookiecutter(
                    template_dir, extra_context={"repo_url": valid_url}, output_dir=temp_dir
                )
                assert Path(project_path).exists(), f"Failed for repo_url: {valid_url}"
            except RuntimeError as e:
                raise AssertionError(f"Unexpected error for repo_url '{valid_url}': {e}") from e

    @pytest.mark.parametrize(
        "invalid_node_version",
        [
            "",
            "v20",
            "20.0",
            "twenty",
        ],
    )
    def test_invalid_node_version(self, invalid_node_version):
        """Test validation of invalid Node.js versions."""
        template_dir = get_template_dir()

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                run_cookiecutter(
                    template_dir, extra_context={"node_version": invalid_node_version}, output_dir=temp_dir
                )
                raise AssertionError(f"Expected validation error for node_version: {invalid_node_version}")
            except RuntimeError as e:
                assert "Hook script failed" in str(e)

    @pytest.mark.parametrize(
        "valid_node_version",
        [
            "18",
            "20",
            "22",
        ],
    )
    def test_valid_node_version(self, valid_node_version):
        """Test validation of valid Node.js versions."""
        template_dir = get_template_dir()

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                project_path = run_cookiecutter(
                    template_dir, extra_context={"node_version": valid_node_version}, output_dir=temp_dir
                )
                assert Path(project_path).exists(), f"Failed for node_version: {valid_node_version}"
            except RuntimeError as e:
                raise AssertionError(f"Unexpected error for node_version '{valid_node_version}': {e}") from e
