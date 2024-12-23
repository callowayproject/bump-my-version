#!/usr/bin/env python
"""
Generate documentation stubs for the configured package.

Configuring this script:

    Change the `package_name` variable to the name of the package you want to generate

Output:

    This script will generate a `reference/api` directory containing documentation stubs for the package.
    It will also generate a `reference/api/SUMMARY.md` file that contains the navigation structure for the
    documentation.
"""

from pathlib import Path

import mkdocs_gen_files

package_name = "bumpversion"

nav = mkdocs_gen_files.Nav()
mod_symbol = '<code class="doc-symbol doc-symbol-nav doc-symbol-module"></code>'

src_root = Path(__file__).parent.parent
package_root = src_root / package_name

for path in sorted(package_root.rglob("*.py")):
    module_path = path.relative_to(src_root).with_suffix("")
    doc_path = path.relative_to(src_root).with_suffix(".md")
    full_doc_path = Path("reference/api", doc_path)

    parts = tuple(module_path.parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1].startswith("_"):
        continue

    nav_parts = [f"{mod_symbol} {part}" for part in parts]
    nav[tuple(nav_parts)] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(parts)
        fd.write(f"::: {ident}")

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open("reference/api/nav.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
