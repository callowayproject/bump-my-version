# Plugin Specifications

## Configuration file

Goals:
- use namespacing to separate configurations
- Allow new configuration sections and keys to be added without breaking plugins
- Multiple plugins can read the same file and return different or partial results
  - For example, a plugin could read a `pyproject.toml` file and return the `project.version` as the `current_version` value.
  - This still allows for other plugins to process the other parts of the configuration


- Discovery: Which file(s) to use
  - change default order of searching for files
  - accept URLs
- Creating: creating or updating an existing configuration file
- Reading: Parsing the configuration data
- Merging: Merging the configuration data from multiple sources
- Post-processing: Using the configuration to modify itself
- Updating: Updating values in the configuration


### Modify default configuration file names

Allows plugins to add two types of names to the top of the search stack.
    - default
    - alternatives
if you prefer it to be .bumpversion.yaml, but will accept .bumpversion.yml

All plugins will be ahead of the default paths, but their order between each other is not guaranteed.

The default names will also be choices for the `sample_config` command.

### Create configuration file

Inputs:

- file path
- initial data (from questions)
- bump-my-version defaults

Outputs:

- Full configuration

Expected behavior:

if the configuration path does not exist, write the initial and default data to it

if the configuration path already exists, update it with the initial data

return the full configuration

### Read config file

Inputs:

- The config file path

Outputs:

- None (if the plugin doesn't support the file)
- configuration

Expected behavior

File paths are discovered before calling plugins. If multiple files are detected, each path is passed to all plugins.

If multiple configuration files have valid configurations, a warning is output to the user. This informs them that bump-my-version is merging the configuration from multiple sources and from which sources it detected. This may or may not be the desired behavior.

Plugins should read in all available data in a section to allow for post-processing and future capabilities.

### Post-process config


### Change config file
