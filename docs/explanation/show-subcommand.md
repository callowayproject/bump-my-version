# The show subcommand

The main purpose of the `show` subcommand is to provide access to configuration data via scripts.

## Basic use

The configuration object is a `dict` containing nested data structures. The arguments and options of this command relate to extracting data from the configuration object and presenting the extracted data. 

## Specifying the output data

The positional arguments determine the data shown. If nothing or `all` is passed, the entire configuration is shown.

Positional arguments are specified using a format like [Django variable resolution](https://docs.djangoproject.com/en/5.0/ref/templates/language/#variables).

Examples:

- `a.b` specifies the "b" key in the nested dictionaries: `{"a": {"b": "value"}}`
- `a.3` specifies the 4th item (the first is 0) of the list at key "a": `{"a": ["no", "nay", "nyet", "value"]}`

## Specifying the output format

If only one positional argument is passed, the default format only shows its value. If no positional arguments, several positional arguments, or `all` is passed, the output from [`pprint.pprint`](https://docs.python.org/3.12/library/pprint.html#pprint.pprint) is shown.

This makes getting the current version easy:

```console
$ bump-my-version show current_version
1.0.1
```

You can request the output be formatted as YAML or JSON:

```console
$ bump-my-version show --format yaml current_version
current_version: "1.0.1"
$ bump-my-version show --format json current_version
{
  "current_version": "1.0.1"
}
```

## Including the incremented version before bumping

Your workflow might want to know the new version before you actually do the bumping. The `--increment` or `-i` option accepts a version part to bump and adds a `new_version` key into the configuration.

```console
$ bump-my-version --increment patch show
1.0.2
$ bump-my-version --increment minor show
1.1.0
$ bump-my-version --increment major show
2.0.0
```
