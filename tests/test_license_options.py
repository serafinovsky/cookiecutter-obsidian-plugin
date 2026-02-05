import pytest
from helpers import (
    assert_file_contains,
    assert_file_exists,
    assert_file_not_exists,
    cleanup_project,
    get_default_context,
    get_template_dir,
    run_cookiecutter,
)


class TestLicenseOptions:
    """Test license option functionality."""

    @pytest.mark.parametrize(
        "license_type,license_text,version_text",
        [
            (
                "MIT",
                "MIT License",
                "Permission is hereby granted",
            ),
            (
                "Apache-2.0",
                "Apache License",
                "Version 2.0",
            ),
            (
                "BSD-3-Clause",
                "BSD 3-Clause License",
                "Redistribution and use",
            ),
            (
                "GPL-3.0",
                "GNU GENERAL PUBLIC LICENSE",
                "Version 3",
            ),
            (
                "ISC",
                "ISC License",
                "Permission to use, copy, modify",
            ),
        ],
    )
    def test_license_generation(self, license_type, license_text, version_text):
        template_dir = get_template_dir()
        context = get_default_context()
        context["license"] = license_type
        project_path = run_cookiecutter(template_dir, context)

        try:
            assert_file_exists(project_path, "LICENSE")

            assert_file_contains(project_path, "LICENSE", license_text)
            assert_file_contains(project_path, "LICENSE", "Test Author")
            assert_file_contains(project_path, "LICENSE", version_text)

            assert_file_contains(project_path, "README.md", license_type)
        finally:
            cleanup_project(project_path)

    def test_no_license(self):
        template_dir = get_template_dir()
        context = get_default_context()
        context["license"] = "none"
        project_path = run_cookiecutter(template_dir, context)

        try:
            assert_file_not_exists(project_path, "LICENSE")

            assert_file_contains(project_path, "README.md", "No license.")
        finally:
            cleanup_project(project_path)
