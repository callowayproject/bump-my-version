import { existsSync, readdirSync, readFileSync } from "node:fs";
import { basename, dirname, join, posix } from "node:path";
import { fileURLToPath } from "node:url";
import { defineConfig, type DefaultTheme } from "vitepress";
import deflist from "markdown-it-deflist";

// The site is served from a subpath on GitHub Pages; PR previews override this.
const base = process.env.DOCS_BASE ?? "/bump-my-version/";
const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const sections = ["tutorials", "howtos", "reference", "explanation"] as const;

/** All markdown files under `dir` as posix paths relative to the docs root. */
function markdownFiles(dir: string): string[] {
  return readdirSync(join(root, dir), { withFileTypes: true }).flatMap((e) => {
    const path = `${dir}/${e.name}`;
    if (e.isDirectory()) return markdownFiles(path);
    return e.name.endsWith(".md") ? [path] : [];
  });
}

/**
 * Emit `foo.md` as `foo/index.html` so the URLs match the old site (`/foo/`).
 * The title helpers below read the source files, so this only affects the output path.
 */
function buildRewrites(): Record<string, string> {
  const rewrites: Record<string, string> = {};
  const pages = [
    ...sections.flatMap((s) => markdownFiles(s)),
    "CHANGELOG.md",
    "CONTRIBUTING.md",
  ];
  for (const page of pages) {
    if (basename(page) !== "index.md") rewrites[page] = page.replace(/\.md$/, "/index.md");
  }
  return rewrites;
}

/** Page title: front matter `title`, else the first heading outside code fences, else the file name. */
function titleOf(file: string): string {
  const text = readFileSync(join(root, file), "utf8");
  const front = text.match(/^---\n([\s\S]*?)\n---/);
  const fmTitle = front?.[1].match(/^title:\s*["']?(.+?)["']?\s*$/m)?.[1];
  if (fmTitle) return fmTitle;
  let inFence = false;
  for (const line of text.split("\n")) {
    if (line.startsWith("```")) inFence = !inFence;
    else if (!inFence && line.startsWith("# ")) return line.slice(2).trim();
  }
  const name = basename(file, ".md").replace(/[-_]/g, " ");
  return name.charAt(0).toUpperCase() + name.slice(1);
}

/** Files linked from `<dir>/index.md`, in link order, if that index is a plain link list. */
function indexOrder(dir: string): string[] {
  const index = join(root, dir, "index.md");
  if (!existsSync(index)) return [];
  return [...readFileSync(index, "utf8").matchAll(/\]\(([^)#]+\.md)\)/g)].map((m) => `${dir}/${m[1]}`);
}

function link(file: string): string {
  const base = file.replace(/\.md$/, "");
  return "/" + (basename(file) === "index.md" ? base.replace(/index$/, "") : base + "/");
}

function sidebarFor(dir: string): DefaultTheme.SidebarItem[] {
  const listed = indexOrder(dir);
  const files = markdownFiles(dir).filter((f) => !f.includes("/api/") && f !== `${dir}/index.md`);
  const rank = (f: string) => {
    const i = listed.indexOf(f);
    return i === -1 ? Infinity : i;
  };
  return files
    .sort((a, b) => rank(a) - rank(b) || a.localeCompare(b))
    .filter((f) => !/\/index\.md$/.test(f))
    .map((f) => ({ text: titleOf(f), link: link(f) }));
}

const rewrites = buildRewrites();
const sourceOf: Record<string, string> = Object.fromEntries(Object.entries(rewrites).map(([src, out]) => [out, src]));

const apiPath =join(root, ".vitepress", "api-sidebar.json");
const apiSidebar: DefaultTheme.SidebarItem[] = existsSync(apiPath) ? JSON.parse(readFileSync(apiPath, "utf8")) : [];

const sidebar: DefaultTheme.Sidebar = {
  "/tutorials/": [{ text: "Tutorials", items: sidebarFor("tutorials") }],
  "/howtos/": [{ text: "How Tos", link: "/howtos/", items: sidebarFor("howtos") }],
  "/explanation/": [{ text: "Explanation", link: "/explanation/", items: sidebarFor("explanation") }],
  "/reference/api/": [
    { text: "Reference", link: "/reference/" },
    { text: "API", items: apiSidebar },
  ],
  "/reference/": [
    {
      text: "Reference",
      link: "/reference/",
      items: [...sidebarFor("reference"), { text: "API", link: "/reference/api/bumpversion/" }],
    },
  ],
};

export default defineConfig({
  title: "Bump My Version",
  description: "Update all version strings in your project and optionally commit and tag the changes.",
  base,
  srcExclude: ["agents/**"],
  rewrites,
  lastUpdated: true,
  head: [["link", { rel: "icon", href: `${base}bump-my-version-logo.svg` }]],
  markdown: {
    config: (md) => {
      md.use(deflist);
      // `foo.md` is emitted as `foo/index.html`, which would resolve relative links one level too deep.
      // Make relative `.md` links absolute from the source location so they are unaffected.
      md.core.ruler.push("absolute-md-links", (state) => {
        // `env.relativePath` is the rewritten path; map it back to the source file.
        const source = sourceOf[state.env.relativePath as string];
        if (!source) return;
        for (const block of state.tokens) {
          for (const token of block.children ?? []) {
            if (token.type !== "link_open") continue;
            const href = token.attrGet("href");
            if (!href || !/^[^/#:][^:]*\.md(#.*)?$/.test(href)) continue;
            token.attrSet("href", posix.join("/", posix.dirname(source), href));
          }
        }
      });
    },
  },
  themeConfig: {
    logo: "/bump-my-version-logo.svg",
    nav: [
      { text: "Tutorials", link: "/tutorials/getting-started/" },
      { text: "How Tos", link: "/howtos/" },
      { text: "Reference", link: "/reference/" },
      { text: "Explanation", link: "/explanation/" },
      { text: "Changelog", link: "/CHANGELOG/" },
      { text: "Contributing", link: "/CONTRIBUTING/" },
    ],
    sidebar,
    search: { provider: "local" },
    editLink: {
      pattern: "https://github.com/callowayproject/bump-my-version/edit/master/docs/:path",
    },
    socialLinks: [{ icon: "github", link: "https://github.com/callowayproject/bump-my-version" }],
    footer: { copyright: "Calloway Project" },
  },
});
