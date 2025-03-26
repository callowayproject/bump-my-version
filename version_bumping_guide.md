---
title: Version Bumping Guide
---

# Version Bumping Guide

Bump My Version is a powerful tool for managing version numbers in your software projects. This guide will walk you through the process of bumping versions, explain different versioning schemes, and show you how to handle dependencies between version components.

## Table of Contents

1. [Understanding Version Components](#understanding-version-components)
2. [Bumping Version Numbers](#bumping-version-numbers)
3. [Versioning Schemes](#versioning-schemes)
4. [Handling Component Dependencies](#handling-component-dependencies)
5. [Advanced Configuration](#advanced-configuration)

## Understanding Version Components

In Bump My Version, a version number is composed of one or more components. Each component can be configured independently and has its own behavior when bumped. The main attributes of a version component are:

- `values`: Possible values for the component (for non-numeric components)
- `optional_value`: A value that can be omitted from the version string
- `first_value`: The initial value of the component
- `independent`: Whether the component is independent of other components
- `always_increment`: Whether the component should always increment, even if not necessary
- `calver_format`: A format string for calendar versioning components

## Bumping Version Numbers

To bump a version number, you specify which component to increment. Bump My Version will handle the rest, including resetting dependent components if necessary. Here's how it works:

1. Specify the component to bump (e.g., "major", "minor", "patch")
2. Bump My Version increments the specified component
3. Any dependent components are reset to their initial values
4. Components configured with `always_increment` are incremented

Example:

```python
from bumpversion.bump import do_bump
from bumpversion.config import Config

config = Config(...)  # Load your configuration
do_bump(version_part="minor", config=config)
```

## Versioning Schemes

Bump My Version supports various versioning schemes:

### Semantic Versioning (SemVer)

For SemVer, you typically have three components: major, minor, and patch. Configure them like this:

```yaml
version_config:
  major:
    independent: false
  minor:
    independent: false
  patch:
    independent: false
```

### Calendar Versioning (CalVer)

For CalVer, use the `calver_format` attribute. For example:

```yaml
version_config:
  year:
    calver_format: "%Y"
  month:
    calver_format: "%m"
  micro:
    independent: false
```

### Custom Versioning

You can create custom versioning schemes by defining your own components and their behaviors.

## Handling Component Dependencies

Version components can have dependencies on each other. When a component is bumped, its dependent components are reset. You can specify dependencies in two ways:

1. Implicit dependencies based on component order
2. Explicit dependencies using the `depends_on` attribute

Example of explicit dependencies:

```yaml
version_config:
  major:
    independent: false
  minor:
    depends_on: major
  patch:
    depends_on: minor
```

## Advanced Configuration

### Always Increment

Use the `always_increment` attribute to make a component increment on every version bump, regardless of which component was specified:

```yaml
version_config:
  build:
    always_increment: true
```

### Optional Components

Set an `optional_value` to make a component optional in the version string:

```yaml
version_config:
  pre:
    values: [alpha, beta, rc]
    optional_value: ""
```

This allows versions like "1.2.3" and "1.2.3-beta" to coexist in your versioning scheme.

Remember to adjust your configuration based on your project's specific needs and versioning requirements.