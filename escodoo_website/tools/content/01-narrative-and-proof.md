# Narrative and proof

## The three layers

The site carries one thesis, backed by one proof, sealed by one credential. Every page
must be traceable to this stack.

### Layer 1 — the thesis: sovereignty

> **EN** Community + OCA is not the cheap Odoo. It is the Odoo you control. **PT**
> Community + OCA não é o Odoo barato. É o Odoo que você controla.

> **EN** Brazil is seven years into a tax transition. Control is worth more than
> convenience. **PT** O Brasil tem sete anos de transição tributária pela frente.
> Controle vale mais que conveniência.

Selling Community on price is the trap to avoid. It validates the framing used by the
largest Odoo partner in the world, which presents Community as what is left for whoever
cannot pay, and it hands the argument to whoever has more cost scale. Sovereignty,
portability and audit are defensible; price is not.

### Layer 2 — the proof: curation

> **EN** We reviewed 794 community contributions in 2025. The code that reaches your ERP
> passed through us before it became standard. **PT** Revisamos 794 contribuições da
> comunidade em 2025. O código que chega ao seu ERP passou por nós antes de virar
> padrão.

This is the strongest and least copyable asset. Review capacity is the scarcest resource
in the OCA: it is what releases or blocks everyone else's code. The ratio is what makes
it unusual — 794 reviews against 96 pull requests created, which is inverted compared to
most of the global top ten. It reframes the credential from volume of output to audited
quality, which is what a risk averse ERP buyer actually wants to hear.

### Layer 3 — the seal: verifiable global authority

> **EN** Two of our engineers rank among the twenty largest contributors to the OCA
> worldwide. Check it yourself. **PT** Dois de nossos engenheiros estão entre os vinte
> maiores contribuidores da OCA no mundo. Confira você mesmo.

## Proof inventory

### Verifiable, with a public source

The OCA stopped publishing statistics officially; the series was restored in a neutral
public repository.

| Fact                                     | Value               | Source                                                                |
| ---------------------------------------- | ------------------- | --------------------------------------------------------------------- |
| `marcelsavegnago` 2025 contributor index | rank 9, CI 878      | `OCA-contributors/monthly-statistics`, `2025/contributors_12_YTD.csv` |
| Reviews vs pull requests, same row       | 794 reviews, 96 PRs | same file                                                             |
| `antoniospneto` 2025 contributor index   | rank 20, CI 428     | same file                                                             |
| Statistics generator                     | open source         | `OCA-contributors/contributors-statistics-generator`                  |
| Monthly rankings naming Escodoo          | e.g. April 2025     | `odoo-community.org` blog                                             |

Canonical link used on the site:
`https://github.com/OCA-contributors/monthly-statistics/blob/main/2025/contributors_12_YTD.csv`

### Wording rule, mandatory

The dataset ranks **individuals**, not companies. The site therefore says "two of our
engineers are among the twenty largest global contributors" and never "Escodoo is the
ninth company". Inflating a verifiable claim destroys the only advantage of having a
verifiable claim.

Equally, the claim of being "certified in Odoo" that appears today on the maintenance
page is dropped unless a certificate can be shown, because official certification
belongs to Odoo S.A.

### Company facts

| Fact            | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Operating since | 2015                                                         |
| Base            | Ribeirão Preto, São Paulo, Brazil                            |
| Coverage        | all of Brazil, remote first                                  |
| Focus           | Odoo Community, OCA ecosystem, Brazilian fiscal localisation |
| Contact         | `contato@escodoo.com.br`, `+55 16 98872-7010`                |

### Numbers to be confirmed before publication

These are placeholders in the copy and are marked in the XML with a comment. Publishing
an unverified number would undo the point of layer 3.

- Projects delivered.
- Modules under maintenance contract, the metric that reads as accepted responsibility
  rather than as output.
- Share of gaps covered by existing OCA modules versus new development, taken from the
  last N projects. This is the number that dissolves the fear of having to build
  everything, and no Western integrator publishes it.
- Client retention expressed as an exchange: how many arrived from another supplier
  against how many left.

## Anonymous cases

Client names, logos and testimonials are not available yet. Cases are published with a
real profile and real numbers, without identification:

> **EN** Metalworking industry, 80 users, inland São Paulo **PT** Indústria
> metalmecânica, 80 usuários, interior de São Paulo

The page template keeps the identification block separate from the metrics so a case can
be named later without reworking the page.

## Tone

- Address a manager, not an IT department. The industry pages already do this well on
  the live site and that voice is preserved.
- State the limits of the recommendation. The comparison page names the cases where
  Enterprise wins. A comparison that admits its own defeats is far more convincing than
  one that does not, and it is precisely what the competing comparison pages avoid.
- No unquantified superlatives. "Infrastructure of global level" without naming a
  provider weakens exactly the reader who cares about latency and data residency.
- Keep the humour that already works in the industry pages. It humanises copy that would
  otherwise read like a press release.

## Recurring pillars, carried over from the live site

These already run consistently through the current site and stay:

1. OCA good practice as a quality guarantee.
2. Sound architecture, sustainable code, no technical debt: we do not deliver screens
   and forms, we structure operations.
3. Predictability and governance, of delivery, of cost and of operation.
4. Freedom and sovereignty, against lock-in.
5. Long term continuity: go live is not the finish line.
6. Process before technology.
