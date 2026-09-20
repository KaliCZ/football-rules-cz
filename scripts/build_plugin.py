"""Validate the canonical skill resources and optionally build a reproducible archive."""
import argparse
import io
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/football-rules-cz"
REFERENCES = PLUGIN / "skills/football-rules-cz/references"
ARCHIVE = ROOT / "dist/football-rules-cz.zip"


def resource_files():
    return [REFERENCES / "rules.md", *sorted((REFERENCES / "assets").glob("*.png")),
            *sorted((REFERENCES / "sources").glob("*.pdf"))]


def verify_links():
    text = (REFERENCES / "rules.md").read_text(encoding="utf-8")
    anchors = set(re.findall(r'<a id="([^"]+)"', text))
    for target in re.findall(r"\]\(([^)]+)\)", text):
        if "://" in target:
            continue
        filename, _, fragment = target.partition("#")
        if filename:
            resolved = (REFERENCES / filename).resolve()
            if not resolved.is_relative_to(REFERENCES) or not resolved.is_file():
                raise ValueError(f"Missing or unsafe reference: {target}")
        elif fragment not in anchors:
            raise ValueError(f"Missing anchor: {target}")


def archive_bytes():
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(PLUGIN.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"Symlinks are not portable: {path}")
            if path.is_file():
                entry = zipfile.ZipInfo(path.relative_to(PLUGIN).as_posix(), (2024, 7, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.external_attr = 0o100644 << 16
                archive.writestr(entry, path.read_bytes(), compresslevel=9)
    return output.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify generated files without changing them")
    args = parser.parse_args()
    resources = resource_files()
    for path in resources:
        if not path.is_file():
            raise ValueError(f"Missing resource: {path}")
    portable = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))
    compatibility = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    claude = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    for key in ("name", "version", "description", "author", "homepage", "repository"):
        if not portable[key] == compatibility[key] == claude[key]:
            raise ValueError(f"Manifest mismatch: {key}")
    if portable["extensions"]["com.openai"]["interface"] != compatibility["interface"]:
        raise ValueError("Manifest interface mismatch")
    marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    entry = next(item for item in marketplace["plugins"] if item["name"] == portable["name"])
    if (ROOT / entry["source"]["path"]).resolve() != PLUGIN:
        raise ValueError("Marketplace points to the wrong plugin directory")
    claude_marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    claude_entry = next(item for item in claude_marketplace["plugins"] if item["name"] == portable["name"])
    if (ROOT / claude_entry["source"]).resolve() != PLUGIN:
        raise ValueError("Claude marketplace points to the wrong plugin directory")
    verify_links()
    print(f"Verified {len(resources)} canonical resources, links, and plugin metadata.")
    if not args.check:
        content = archive_bytes()
        ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
        ARCHIVE.write_bytes(content)
        print(f"Built {ARCHIVE.relative_to(ROOT)} ({len(content):,} bytes).")



if __name__ == "__main__":
    main()
