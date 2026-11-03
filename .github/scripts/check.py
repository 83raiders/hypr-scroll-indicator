#!/usr/bin/env python3
"""Validate the plugin source: manifests parse, catalog matches, required files exist."""
import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERSION_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*/[a-z0-9][a-z0-9._-]*$")
REQUIRED = ["plugin.toml", "README.md", "translations/en.json", "thumbnail.webp"]

errors = []


def err(msg):
    errors.append(msg)
    print(f"ERROR: {msg}")


catalog = tomllib.loads((ROOT / "catalog.toml").read_text())
rows = {row["id"]: row for row in catalog.get("plugin", [])}

for manifest_path in sorted(ROOT.glob("*/plugin.toml")):
    plugin_dir = manifest_path.parent
    m = tomllib.loads(manifest_path.read_text())
    pid = m.get("id", "")
    print(f"checking {pid} ({plugin_dir.name}/)")

    for key in ("id", "name", "version", "plugin_api"):
        if key not in m:
            err(f"{manifest_path}: missing '{key}'")
    if not ID_RE.match(pid):
        err(f"{manifest_path}: bad id '{pid}'")
    elif pid.split("/", 1)[1] != plugin_dir.name:
        err(f"{manifest_path}: id '{pid}' must match directory '{plugin_dir.name}'")
    if not VERSION_RE.match(str(m.get("version", ""))):
        err(f"{manifest_path}: version must be MAJOR.MINOR.PATCH")
    if not isinstance(m.get("plugin_api"), int) or m["plugin_api"] < 1:
        err(f"{manifest_path}: plugin_api must be a positive integer")

    for rel in REQUIRED:
        if not (plugin_dir / rel).exists():
            err(f"{plugin_dir.name}/{rel} is missing")
    for entry in m.get("widget", []):
        if not (plugin_dir / entry.get("entry", "")).exists():
            err(f"{plugin_dir.name}/{entry.get('entry')} (widget entry) is missing")

    tr = plugin_dir / "translations" / "en.json"
    if tr.exists():
        try:
            json.loads(tr.read_text())
        except json.JSONDecodeError as e:
            err(f"{tr}: invalid JSON: {e}")

    row = rows.get(pid)
    if row is None:
        err(f"catalog.toml has no row for {pid}")
    else:
        for key in ("version", "plugin_api", "name"):
            if row.get(key) != m.get(key):
                err(f"catalog.toml {key}={row.get(key)!r} does not match plugin.toml {m.get(key)!r}")

if errors:
    sys.exit(f"{len(errors)} problem(s) found")
print("all checks passed")
