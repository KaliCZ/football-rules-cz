"""Validate the canonical skill resources and optionally build a reproducible archive."""
import argparse
import io
import hashlib
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/football-rules-cz"
REFERENCES = SKILL / "references"


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
        for path in sorted(SKILL.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"Symlinks are not portable: {path}")
            if path.is_file():
                entry = zipfile.ZipInfo("football-rules-cz/" + path.relative_to(SKILL).as_posix(), (2024, 7, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.external_attr = 0o100644 << 16
                archive.writestr(entry, path.read_bytes(), compresslevel=9)
    return output.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify generated files without changing them")
    parser.add_argument("--version", help="Required for builds, in MAJOR.MINOR.PATCH format (for example 0.2.1)")
    args = parser.parse_args()
    if not args.check and args.version is None:
        parser.error("--version is required when building an archive")
    if args.version is not None and not re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", args.version):
        parser.error("--version must use MAJOR.MINOR.PATCH format, for example 0.2.1")
    resources = resource_files()
    for path in resources:
        if not path.is_file():
            raise ValueError(f"Missing resource: {path}")
    skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    if not skill_text.startswith("---\nname: football-rules-cz\n"):
        raise ValueError("Skill folder and frontmatter name must agree")
    for path in SKILL.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"Symlinks are not portable: {path}")
    verify_links()
    print(f"Verified {len(resources)} canonical resources, links, and skill structure.")
    if not args.check:
        archive = ROOT / "dist" / f"football-rules-cz-skill-{args.version}.zip"
        content = archive_bytes()
        archive.parent.mkdir(parents=True, exist_ok=True)
        archive.write_bytes(content)
        checksum = hashlib.sha256(content).hexdigest()
        (archive.parent / "SHA256SUMS.txt").write_text(
            f"{checksum}  {archive.name}\n", encoding="utf-8", newline="\n")
        print(f"Built {archive.relative_to(ROOT)} ({len(content):,} bytes).")



if __name__ == "__main__":
    main()
