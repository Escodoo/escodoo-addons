# Content specification

This folder is the authoring source of truth for the public site copy. It is **not**
loaded by Odoo — the addon manifest never references `tools/`.

## Why it exists

The repository requires English source code, so every user visible string lives in
`data/website_view_*.xml` as `en_US` and reaches the visitor through `i18n/pt_BR.po`.
Brazil is the primary market, so writing English first and translating afterwards would
turn the commercially relevant wording into a literal translation.

The workflow is therefore:

1. Author the message in Portuguese here, where it can be reviewed by whoever owns
   positioning.
2. Derive the English source string, kept side by side in the same file.
3. Implement the English string in the page XML.
4. Feed the pair into `tools/build_i18n_pt_br.py`, which writes `i18n/pt_BR.po`.

Every strategic string is listed as a `EN | PT` pair so the mapping used by the
translation builder stays auditable.

## Files

| File                             | Content                                                     |
| -------------------------------- | ----------------------------------------------------------- |
| `00-information-architecture.md` | Menu, page inventory, URL map and the 301 redirects         |
| `01-narrative-and-proof.md`      | Narrative layers, the proof inventory and the wording rules |
| `02-positioning-hub.md`          | "Why Community + OCA" pages                                 |
| `03-solutions-and-services.md`   | Solution and service pages                                  |
| `04-segments.md`                 | The seven industry pages                                    |
| `05-company-and-cases.md`        | Company, cases, FAQ and international                       |
| `06-conversion.md`               | Forms, thank-you pages and lead routing                     |
