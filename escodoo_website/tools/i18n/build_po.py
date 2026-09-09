#!/usr/bin/env python3
"""Build ``i18n/pt_BR.po`` from the exported template and the glossary files.

The source language is English and the public site is served in Portuguese, so
the PO file is not a nicety: an untranslated entry ships English copy to a
Brazilian reader. That makes the coverage report below the point of this script.

Translations are authored in ``tools/i18n/pt_BR/*.json`` as a plain mapping of
source string to translation. The ``msgid`` values themselves are always copied
from the template rather than retyped, because a single character of drift makes
a translation silently inert.

Usage, from the addon root::

    python3 tools/i18n/build_po.py            # write i18n/pt_BR.po
    python3 tools/i18n/build_po.py --check    # report coverage, write nothing
"""

# A command line tool run by a developer, never imported by Odoo, so the
# coverage report belongs on stdout rather than in the server log.
# pylint: disable=print-used

import argparse
import json
import pathlib
import re
import sys

ADDON_ROOT = pathlib.Path(__file__).resolve().parents[2]
POT_PATH = ADDON_ROOT / "i18n" / "escodoo_website.pot"
PO_PATH = ADDON_ROOT / "i18n" / "pt_BR.po"
GLOSSARY_DIR = pathlib.Path(__file__).resolve().parent / "pt_BR"

PO_HEADER = """# Translation of Odoo Server.
# This file contains the translation of the following modules:
# \t* escodoo_website
#
msgid ""
msgstr ""
"Project-Id-Version: Odoo Server 18.0\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2026-08-28 06:35+0000\\n"
"PO-Revision-Date: 2026-08-28 06:35+0000\\n"
"Last-Translator: Escodoo <contato@escodoo.com.br>\\n"
"Language-Team: Portuguese (Brazil)\\n"
"Language: pt_BR\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: \\n"
"Plural-Forms: \\n"
"""

STRING_RE = re.compile(r'"((?:[^"\\]|\\.)*)"')


ESCAPES = {"n": "\n", "t": "\t", "r": "\r", '"': '"', "\\": "\\"}


def unquote(block):
    """Join a PO multi-line string back into one value, resolving escapes.

    Terms taken from a QWeb arch keep the line breaks and indentation of the
    XML, so the escapes have to be resolved and re-emitted identically or the
    ``msgid`` stops matching the template.
    """
    raw = "".join(STRING_RE.findall(block))
    return re.sub(r"\\(.)", lambda m: ESCAPES.get(m.group(1), m.group(0)), raw)


def quote(value):
    """Render a value as PO string lines, splitting on sentence boundaries.

    Odoo's own exporter emits one long line, and matching that keeps the diff
    between template and translation readable.
    """
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{escaped}"'


def parse_pot(text):
    """Yield ``(comment_block, msgid)`` in template order."""
    chunks = text.split("\n\n")
    for chunk in chunks:
        if "\nmsgid " not in f"\n{chunk}":
            continue
        match = re.search(r"(?ms)^msgid ((?:\".*\"\s*)+?)^msgstr", chunk + "\n")
        if not match:
            continue
        msgid = unquote(match.group(1))
        if not msgid:
            continue
        comment = chunk[: match.start()].rstrip("\n")
        yield comment, msgid


def lookup_key(value):
    """Normalise a term for glossary lookup.

    Terms extracted from a QWeb arch carry the line breaks and indentation of
    the XML, so keying the glossary on the raw value would mean authoring
    translations against invisible whitespace and re-authoring them whenever a
    template is reformatted. Collapsing runs of whitespace keeps the glossary
    readable and stable; the ``msgid`` written to the PO file is still the exact
    template value.
    """
    return " ".join(value.split())


def load_glossary():
    glossary = {}
    if not GLOSSARY_DIR.is_dir():
        return glossary
    for path in sorted(GLOSSARY_DIR.glob("*.json")):
        with path.open(encoding="utf-8") as handle:
            entries = json.load(handle)
        for source, translation in entries.items():
            key = lookup_key(source)
            if key in glossary and glossary[key] != translation:
                raise SystemExit(f"{path.name}: conflicting translation for {key!r}")
            glossary[key] = translation
    return glossary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if not POT_PATH.exists():
        raise SystemExit(f"missing template: {POT_PATH}")

    glossary = load_glossary()
    entries = list(parse_pot(POT_PATH.read_text(encoding="utf-8")))
    missing = []
    blocks = []
    for comment, msgid in entries:
        translation = glossary.get(lookup_key(msgid), "")
        if not translation:
            missing.append(lookup_key(msgid))
        blocks.append(
            "\n".join(
                part
                for part in (
                    comment,
                    f"msgid {quote(msgid)}",
                    f"msgstr {quote(translation)}",
                )
                if part
            )
        )

    unused = sorted(set(glossary) - {lookup_key(msgid) for _comment, msgid in entries})
    covered = len(entries) - len(missing)
    print(f"entries: {len(entries)}  translated: {covered}  missing: {len(missing)}")
    if unused:
        print(f"glossary entries not in the template: {len(unused)}")
        for source in unused[:20]:
            print(f"  stale: {source!r}")
    if missing:
        for source in missing[:40]:
            print(f"  missing: {source!r}")

    if args.check:
        return 1 if missing or unused else 0

    PO_PATH.write_text(PO_HEADER + "\n" + "\n\n".join(blocks) + "\n", encoding="utf-8")
    print(f"written: {PO_PATH.relative_to(ADDON_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
