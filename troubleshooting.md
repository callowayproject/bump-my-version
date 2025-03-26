---
title: Troubleshooting
---

# Troubleshooting

This guide will help you resolve common issues you might encounter when using Bump My Version. We'll cover various error messages, their potential causes, and steps to resolve each issue.

## Table of Contents

1. [Configuration Errors](#configuration-errors)
2. [Version Not Found Errors](#version-not-found-errors)
3. [Dirty Working Directory Errors](#dirty-working-directory-errors)
4. [Invalid Version Part Errors](#invalid-version-part-errors)
5. [Hook Errors](#hook-errors)
6. [Missing File Errors](#missing-file-errors)

## Configuration Errors

### Error: ConfigurationError

This error occurs when there's an issue with your Bump My Version configuration.

Possible causes:
- Missing required configuration keys
- Incorrect value types for configuration options

Resolution steps:
1. Check your configuration file (e.g., `.bumpversion.toml` or `pyproject.toml`) for any missing required keys.
2. Ensure all configuration values are of the correct type (e.g., strings, booleans, lists).
3. Run `bump-my-version show` to display your current configuration and verify its correctness.
4. If you're unsure about the correct configuration format, use `bump-my-version sample-config` to generate a sample configuration file.

## Version Not Found Errors

### Error: VersionNotFoundError

This error occurs when Bump My Version can't find the current version in one of the specified files.

Possible causes:
- Incorrect `parse` regex in the configuration
- The version string is not present in the specified file
- The `search` pattern doesn't match the version string in the file

Resolution steps:
1. Verify that the version string is present in the specified files.
2. Check your `parse` regex in the configuration to ensure it correctly matches your version format.
3. If you're using a custom `search` pattern, make sure it accurately represents the string containing the version.
4. Use the `--verbose` option to see more detailed information about where Bump My Version is looking for the version.

Example configuration fix:

```toml
[tool.bumpversion]
current_version = "1.2.3"
parse = "(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)"
serialize = ["{major}.{minor}.{patch}"]
search = "version = \"{current_version}\""
replace = "version = \"{new_version}\""
```

## Dirty Working Directory Errors

### Error: DirtyWorkingDirectoryError

This error occurs when you try to bump the version with uncommitted changes in your working directory.

Resolution steps:
1. Commit or stash your changes before running Bump My Version.
2. If you want to allow bumping the version with a dirty working directory, use the `--allow-dirty` option:

```bash
bump-my-version bump patch --allow-dirty
```

3. Alternatively, you can set `allow_dirty = true` in your configuration file:

```toml
[tool.bumpversion]
allow_dirty = true
```

## Invalid Version Part Errors

### Error: InvalidVersionPartError

This error occurs when you specify an invalid version part to bump.

Resolution steps:
1. Check the available version parts in your configuration.
2. Use one of the defined version parts when bumping the version.

Example:

```bash
# Correct usage
bump-my-version bump patch

# Incorrect usage
bump-my-version bump invalid_part
```

## Hook Errors

### Error: HookError

This error occurs when a pre-defined hook fails during the version bumping process.

Resolution steps:
1. Check the error message for details about which hook failed.
2. Review your hook scripts for any issues.
3. Ensure that all required dependencies for your hooks are installed.
4. Test your hooks independently to verify they work as expected.

## Missing File Errors

If Bump My Version can't find a file specified in your configuration or command line arguments, it will raise an error.

Resolution steps:
1. Verify that all files specified in your configuration or command line arguments exist.
2. Check file paths and ensure they are correct relative to your working directory.
3. If you want to ignore missing files, use the `--ignore-missing-files` option:

```bash
bump-my-version bump patch --ignore-missing-files
```

4. Alternatively, set `ignore_missing_files = true` in your configuration:

```toml
[tool.bumpversion]
ignore_missing_files = true
```

By following this troubleshooting guide, you should be able to resolve most common issues encountered when using Bump My Version. If you continue to experience problems, please check the project's issue tracker or reach out to the community for further assistance.