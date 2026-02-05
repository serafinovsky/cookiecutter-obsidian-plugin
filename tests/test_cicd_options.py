from helpers import (
    assert_file_contains,
    assert_file_exists,
    assert_file_not_contains,
    cleanup_project,
    get_default_context,
    get_template_dir,
    run_cookiecutter,
)


class TestCICDOptions:
    """Test CI/CD workflow generation."""

    def test_ci_files_exist(self):
        """Test GitHub workflow files exist."""
        template_dir = get_template_dir()
        context = get_default_context()

        project_path = run_cookiecutter(template_dir, context)

        try:
            # Check that GitHub Actions files exist
            assert_file_exists(project_path, ".github/workflows/ci.yml")
            assert_file_exists(project_path, ".github/workflows/release.yml")
            assert_file_exists(project_path, ".github/dependabot.yml")
        finally:
            cleanup_project(project_path)

    def test_ci_uses_node_version(self):
        """Test that workflows use configured Node.js version."""
        template_dir = get_template_dir()
        context = get_default_context()
        context["node_version"] = "22"
        project_path = run_cookiecutter(template_dir, context)
        try:
            assert_file_contains(project_path, ".github/workflows/ci.yml", 'node-version: "22"')
            assert_file_contains(project_path, ".github/workflows/release.yml", 'node-version: "22"')
        finally:
            cleanup_project(project_path)

    def test_ci_includes_tests_when_enabled(self):
        """Test that CI includes tests when Vitest is enabled."""
        template_dir = get_template_dir()
        context = get_default_context()
        context["enable_vitest"] = "yes"

        project_path = run_cookiecutter(template_dir, context)

        try:
            assert_file_contains(project_path, ".github/workflows/ci.yml", "npm run test")
        finally:
            cleanup_project(project_path)

    def test_ci_skips_tests_when_disabled(self):
        """Test that CI skips tests when Vitest is disabled."""
        template_dir = get_template_dir()
        context = get_default_context()
        context["enable_vitest"] = "no"
        project_path = run_cookiecutter(template_dir, context)
        try:
            assert_file_not_contains(project_path, ".github/workflows/ci.yml", "npm run test")
        finally:
            cleanup_project(project_path)
