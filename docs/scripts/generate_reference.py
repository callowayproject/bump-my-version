"""
Generate the CLI and API reference pages for the VitePress site.

Writes `reference/cli.md`, `reference/api/**` and `.vitepress/api-sidebar.json` under `docs/`.
All of these are gitignored; run via `npm run gen` (also done by `npm run build`).
"""

import inspect
import json
import shutil
from pathlib import Path

import click
import griffe

DOCS = Path(__file__).resolve().parent.parent
ROOT = DOCS.parent
API_DIR = DOCS / "reference" / "api"
PACKAGE = "bumpversion"

CLI_INTRO = """\
# CLI Reference

Without `--config-file`, the configuration file is searched for in the current directory and, inside a git or \
mercurial repository, each parent directory up to the repository root. See \
[Configuration files](configuration/index.md#configuration-files).

File paths given on the command line are relative to the current working directory; absolute paths are used as-is. \
Paths in the configuration file are relative to the configuration file's directory. See \
[How file paths are resolved](configuration/file.md#how-file-paths-are-resolved).

"""


def _cell(text: str) -> str:
    """Make text safe for a Markdown table cell."""
    return " ".join(text.split()).replace("|", "\\|")


def _render_command(cmd: click.Command, prog: str, level: int) -> str:
    """Render one command (and its subcommands) as Markdown."""
    ctx = click.Context(cmd, info_name=prog)
    out = [f"{'#' * level} {prog}\n"]
    if cmd.help:
        out.append(f"{inspect.cleandoc(click.unstyle(cmd.help))}\n")
    out.append(f"**Usage**\n\n```text\n{' '.join([prog, *cmd.collect_usage_pieces(ctx)])}\n```\n")

    options = [p for p in cmd.get_params(ctx) if isinstance(p, click.Option)]
    if options:
        out.append("**Options**\n\n| Name | Description |\n| --- | --- |")
        for opt in options:
            names = " / ".join(f"`{n}`" for n in [*opt.opts, *opt.secondary_opts])
            out.append(f"| {names} | {_cell(opt.help or '')} |")
        out.append("")

    arguments = [p for p in cmd.get_params(ctx) if isinstance(p, click.Argument)]
    if arguments:
        out.append("**Arguments**\n\n" + "\n".join(f"- `{a.human_readable_name}`" for a in arguments) + "\n")

    if isinstance(cmd, click.Group):
        for name in cmd.list_commands(ctx):
            sub = cmd.get_command(ctx, name)
            if sub is not None and not sub.hidden:
                out.append(_render_command(sub, f"{prog} {name}", level + 1))
    return "\n".join(out)


def write_cli() -> None:
    """Write `reference/cli.md`."""
    from bumpversion.cli import cli

    page = CLI_INTRO + "::: v-pre\n\n" + _render_command(cli, "bump-my-version", 2) + "\n:::\n"
    (DOCS / "reference" / "cli.md").write_text(page)


def _signature(obj: griffe.Object) -> str:
    """Return a one-line Python signature for a class or function."""
    if isinstance(obj, griffe.Class):
        init = obj.members.get("__init__")
        params = init.parameters if init is not None and not init.is_alias else None
        prefix = "class "
    else:
        params = obj.parameters
        prefix = "def "
    args = ""
    if params is not None:
        parts = [p for p in params if p.name not in ("self", "cls")]
        args = ", ".join(
            p.name + (f": {p.annotation}" if p.annotation else "") + (f" = {p.default}" if p.default else "")
            for p in parts
        )
    returns = f" -> {obj.returns}" if isinstance(obj, griffe.Function) and obj.returns else ""
    return f"{prefix}{obj.name}({args}){returns}"


def _docstring(obj: griffe.Object) -> str:
    """Render a parsed Google-style docstring as Markdown."""
    if not obj.docstring:
        return ""
    out = []
    for section in obj.docstring.parse("google"):
        kind = section.kind.value
        if kind == "text":
            out.append(section.value.strip())
        elif kind in ("parameters", "other parameters", "attributes"):
            items = "\n".join(f"- `{p.name}`: {' '.join((p.description or '').split())}" for p in section.value)
            out.append(f"**{section.title or kind.title()}**\n\n{items}")
        elif kind == "returns":
            items = "\n".join(f"- {' '.join((r.description or '').split())}" for r in section.value)
            out.append(f"**Returns**\n\n{items}")
        elif kind == "raises":
            items = "\n".join(f"- `{r.annotation}`: {' '.join((r.description or '').split())}" for r in section.value)
            out.append(f"**Raises**\n\n{items}")
        elif kind == "examples":
            body = "\n\n".join(text if k.value == "text" else f"```python\n{text}\n```" for k, text in section.value)
            out.append(f"**Examples**\n\n{body}")
        elif isinstance(section.value, str):
            out.append(section.value.strip())
    return "\n\n".join(s for s in out if s)


def _render_member(obj: griffe.Object, level: int) -> str:
    """Render a class, function or attribute and (for classes) its public members."""
    kind = "class" if obj.is_class else "function" if obj.is_function else "attribute"
    out = [f"{'#' * level} `{obj.name}` {{#{obj.path.replace('.', '-')}}}\n"]
    if obj.is_class or obj.is_function:
        out.append(f"```python\n{_signature(obj)}\n```\n")
    elif obj.is_attribute:
        out.append(
            f"```python\n{obj.name}{f': {obj.annotation}' if obj.annotation else ''}"
            f"{f' = {obj.value}' if obj.value is not None else ''}\n```\n"
        )
    if doc := _docstring(obj):
        out.append(doc + "\n")
    if kind == "class":
        for member in obj.members.values():
            if member.is_alias or member.name.startswith("_") or member.is_module or member.is_class:
                continue
            if member.docstring or member.is_function:
                out.append(_render_member(member, level + 1))
    return "\n".join(out)


def _is_public(member: griffe.Object | griffe.Alias) -> bool:
    """Whether a module member is a documented-by-default public object (not private, imported, or a submodule)."""
    return not member.name.startswith("_") and not member.is_alias and not member.is_module


def _render_module(mod: griffe.Module) -> str:
    """Render a module page."""
    out = [f"# {mod.path}\n", "::: v-pre\n"]
    if doc := _docstring(mod):
        out.append(doc + "\n")
    members = [m for m in mod.members.values() if _is_public(m)]
    out.extend(_render_member(m, 2) for m in members)
    out.append(":::\n")
    return "\n".join(out)


def _walk(mod: griffe.Module) -> dict:
    """Write pages for a module tree and return its sidebar item."""
    rel = Path(*mod.path.split("."))
    is_package = mod.is_package
    page = API_DIR / rel / "index.md" if is_package else API_DIR / rel.with_suffix(".md")
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(_render_module(mod))
    link = f"/reference/api/{rel.as_posix()}/"
    item: dict = {"text": mod.name, "link": link}
    children = [_walk(m) for m in mod.members.values() if not m.is_alias and m.is_module and not m.name.startswith("_")]
    if children:
        item["items"] = children
        item["collapsed"] = True
    return item


def write_api() -> None:
    """Write `reference/api/**` and the sidebar JSON."""
    if API_DIR.exists():
        shutil.rmtree(API_DIR)
    package = griffe.load(PACKAGE, search_paths=[ROOT])
    sidebar = _walk(package)
    (DOCS / ".vitepress").mkdir(exist_ok=True)
    (DOCS / ".vitepress" / "api-sidebar.json").write_text(json.dumps([sidebar], indent=2))


if __name__ == "__main__":
    write_cli()
    write_api()
