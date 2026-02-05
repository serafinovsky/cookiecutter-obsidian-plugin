import re
import sys


def validate_plugin_id(plugin_id):
    """Validate plugin id for folder name and manifest id."""
    if not plugin_id or not plugin_id.strip():
        return False, "Plugin id cannot be empty"

    if not re.match(r"^[a-z][a-z0-9-]*$", plugin_id.strip()):
        return (
            False,
            "Plugin id must start with a letter and contain only lowercase letters, numbers, and hyphens",
        )

    return True, ""


def validate_plugin_name(name):
    """Validate plugin display name."""
    if not name or not name.strip():
        return False, "Plugin name cannot be empty"

    if not re.match(r"^[a-zA-Z][a-zA-Z0-9\s\-_]*$", name.strip()):
        return (
            False,
            "Plugin name must start with a letter and contain only letters, numbers, spaces, hyphens, and underscores",
        )

    return True, ""


def validate_min_obsidian_version(version):
    """Validate min Obsidian version string."""
    if not version or not version.strip():
        return False, "Minimum Obsidian version cannot be empty"

    if not re.match(r"^\d+\.\d+\.\d+$", version.strip()):
        return False, "Minimum Obsidian version must be in the format X.Y.Z"

    return True, ""


def validate_repo_url(url):
    """Validate repository URL."""
    if not url or not url.strip():
        return False, "Repository URL cannot be empty"

    if not re.match(r"^https://github\.com/", url.strip()):
        return False, "Repository URL must be a GitHub HTTPS URL (https://github.com/...)"

    return True, ""


def validate_node_version(version):
    """Validate Node.js version."""
    if not version or not version.strip():
        return False, "Node.js version cannot be empty"

    if not re.match(r"^\d+$", version.strip()):
        return False, "Node.js version must be a major version number (e.g., 20)"

    return True, ""


# Validate plugin_id
plugin_id = "{{cookiecutter.plugin_id}}"
is_valid, error_msg = validate_plugin_id(plugin_id)
if not is_valid:
    sys.stderr.write(f"ERROR: {error_msg}\n")
    sys.exit(1)

# Validate plugin_name
plugin_name = "{{cookiecutter.plugin_name}}"
is_valid, error_msg = validate_plugin_name(plugin_name)
if not is_valid:
    sys.stderr.write(f"ERROR: {error_msg}\n")
    sys.exit(1)

# Validate min_obsidian_version
min_obsidian_version = "{{cookiecutter.min_obsidian_version}}"
is_valid, error_msg = validate_min_obsidian_version(min_obsidian_version)
if not is_valid:
    sys.stderr.write(f"ERROR: {error_msg}\n")
    sys.exit(1)

# Validate repo_url
repo_url = "{{cookiecutter.repo_url}}"
is_valid, error_msg = validate_repo_url(repo_url)
if not is_valid:
    sys.stderr.write(f"ERROR: {error_msg}\n")
    sys.exit(1)

# Validate node_version
node_version = "{{cookiecutter.node_version}}"
is_valid, error_msg = validate_node_version(node_version)
if not is_valid:
    sys.stderr.write(f"ERROR: {error_msg}\n")
    sys.exit(1)
