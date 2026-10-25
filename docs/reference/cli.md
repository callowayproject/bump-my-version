# CLI Reference

Without `--config-file`, the configuration file is searched for in the current directory and, inside a git or mercurial repository, each parent directory up to the repository root. See [Configuration files](configuration/index.md#configuration-files).

File paths given on the command line are relative to the current working directory; absolute paths are used as-is. Paths in the configuration file are relative to the configuration file's directory. See [How file paths are resolved](configuration/file.md#how-file-paths-are-resolved).

::: mkdocs-click
    :module: bumpversion.cli
    :command: cli
    :prog_name: bump-my-version
    :style: table
    :list_subcommands: true
