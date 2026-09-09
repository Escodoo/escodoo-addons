# Solutions and services

Solutions are named after the buyer's situation; services are named after what we sell.
The same delivery capability appears in both, addressed differently.

## `/implantacao-odoo` — implementation

Rewrite. The six step method is good and stays. What it lacks is everything a buyer
needs to take the decision internally.

| Block       | EN                                                                                                                   | PT                                                                                                                         |
| ----------- | -------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Headline    | Odoo implementation with a predictable path                                                                          | Implantação do Odoo com caminho previsível                                                                                 |
| Subheadline | Structured architecture, OCA good practice, and a delivery plan with dates, deliverables and named responsibilities. | Arquitetura estruturada, boas práticas da OCA, e um plano de entrega com prazos, entregáveis e responsabilidades nomeadas. |

Added: typical duration per phase, the deliverable that closes each phase, what the
client's team has to provide, and an investment range linked to `/investimento`.

Removed: the six generic differentiator cards. "Experienced consulting" and "business
vision" could sit on any competitor's site. They are replaced by checkable statements —
code review on every merge, tests, CI, upstream contribution policy — which is what a
top ten OCA contributor can actually claim and what the current site never mentions.

Also fixed: the duplicated `<h1>` and the `integração c m` typo.

## `/resgate-de-projeto-odoo` — rescue

New. The offer nobody in Brazil names explicitly.

| EN                                                                                                    | PT                                                                                                      |
| ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Your Odoo project stalled. It is recoverable.                                                         | Seu projeto de Odoo travou. Ele é recuperável.                                                          |
| We take over projects in progress, with full or partial recovery of your data and your configuration. | Assumimos projetos em andamento, com recuperação total ou parcial dos seus dados e da sua configuração. |

Blocks: the symptoms of a stalled project, what the assessment covers, what we can and
cannot recover, how the handover from the previous supplier works, and the commercial
format. Entry point is the paid, small, fixed scope assessment, not a full project.

## `/migracao-de-versao-odoo` — version upgrade

New, split out of the old combined infrastructure page where two distinct offers
competed for one URL.

| EN                                                                     | PT                                                                    |
| ---------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Upgrade without trauma                                                 | Upgrade sem trauma                                                    |
| Whoever upgrades best is whoever wrote the migration scripts upstream. | Quem migra melhor é quem escreveu os scripts de migração no upstream. |

The commercial mechanism that already differentiates on the live site is kept and made
prominent, because it answers the single biggest objection to adopting open source —
fear of an expensive upgrade:

| EN                                                                                         | PT                                                                                          |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| The upgrade cost is spread across the monthly fee, not charged as a shock every few years. | O custo do upgrade é diluído na mensalidade, não cobrado como um choque a cada poucos anos. |

Added: a paid pre-upgrade diagnostic as a small deliverable, and the estimate driver
stated plainly — the number of non standard modules.

## `/migrar-para-odoo` — leaving Totvs, SAP or a legacy ERP

New. High value keyword with no coverage today, even though the quote form already lists
this demand as an option.

| EN                                                                              | PT                                                                            |
| ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Moving off Totvs, SAP or a legacy system                                        | Saindo do Totvs, do SAP ou de um sistema legado                               |
| When to change, what carries over, what does not, and how long it really takes. | Quando trocar, o que vem junto, o que não vem, e quanto tempo realmente leva. |

Blocks: the signals that it is time, what data migrates and at what fidelity, the fiscal
history question, running both systems in parallel, and the risks stated openly.

## `/padronizacao-odoo` — standardisation

New, and the most differentiated of the set because nobody sells it explicitly.

| EN                                                                                                | PT                                                                                              |
| ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Replace proprietary customisation with community modules                                          | Troque customização proprietária por módulos da comunidade                                      |
| Measured before and after: lines of custom code, modules off the standard, and your upgrade risk. | Medido antes e depois: linhas de código custom, módulos fora do padrão, e seu risco de upgrade. |

This is the service that converts the OCA credential directly into a client outcome, and
it sells well to anyone already burned by a heavily customised installation.

## `/reforma-tributaria-odoo` — tax reform

New, with a deliberately different angle. A direct Brazilian competitor already owns
"who builds the localisation", with a landing page carrying the 2026 to 2033 timeline
and the actual OCA pull requests. Competing on that ground is playing on their field.
Two angles are open:

**Readiness audit as a small paid product.** Scope and price fixed, deliverable named:
an audit of NCM, CFOP and CST records plus the old to new mapping.

| EN                                                 | PT                                                                       |
| -------------------------------------------------- | ------------------------------------------------------------------------ |
| Tax reform readiness audit                         | Auditoria de prontidão para a Reforma Tributária                         |
| Fixed scope, fixed price, a report you can act on. | Escopo fechado, preço fechado, um relatório sobre o qual você pode agir. |

**Reform as the upgrade trigger.** IBS and CBS support lands first on the newer
versions, so anyone still on an older Odoo has a regulatory deadline that converts into
an upgrade decision. This is the bridge between this page and
`/migracao-de-versao-odoo`, and it is not being used by anyone.

Factual base for the copy: the transition runs from the 2026 test rate through the end
of the old system in 2033, and the argument that holds is structural — the fiscal tax
model in the Brazilian localisation is generic by design, so the new taxes enter as new
records rather than as a rewrite of the fiscal engine.

## `/consultoria-e-desenvolvimento` — consulting and development

Near total rewrite. The current page is the weakest on the site: six cards that restate
flexibility in press release language, and not a single technical specific — which is
counterintuitive for a top ten OCA contributor.

| EN                                                                                                                  | PT                                                                                                                          |
| ------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Development that survives the next upgrade                                                                          | Desenvolvimento que sobrevive ao próximo upgrade                                                                            |
| Code review on every merge, automated tests, continuous integration, and a policy of pushing generic work upstream. | Code review em cada merge, testes automatizados, integração contínua, e política de levar o que é genérico para o upstream. |

Blocks: how we decide between an existing community module and new development — and the
honest rule that if a module already solves it we do not sell development; the
engineering standard; the contracting models with the hour package mechanics; and named
examples of customisations and integrations.

## `/manutencao-odoo` — support and maintenance

Rewrite into a product page. This is the highest lifetime value offer on the site and
the current page gives the buyer nothing comparable to take to an internal approval.

Added: plan tiers, a numeric SLA per severity, coverage windows, the formal channels,
and the price mechanism. Also a working CTA, since the closing block today says "contact
us" with no button or form at all.

## `/hospedagem-odoo` — hosting and infrastructure

New, split out. Keeps the two genuine differentiators from the old page, around the
clock monitoring and the spread upgrade cost, and fixes the vagueness that undermines
exactly the reader who cares: the providers are named, and the page states contractual
uptime, backup frequency and retention, and recovery objectives.

## `/arquitetura-de-processos` — process architecture

Kept almost as is. It is the most mature page on the site and the most executive in
tone, with named methodologies and deliverables. Fixes: the `Durante Durante`
duplication, the empty headings used as spacers, and the three things it never says —
how long it takes, in what format, and how the deliverable connects commercially to the
ERP project afterwards.

## `/segunda-opiniao` — second opinion

New, and the lowest friction entry point on the site. It also inherits the strong angle
abandoned by the old journey page after one paragraph.

| EN                                                                                                                   | PT                                                                                                                        |
| -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| A second opinion on your Odoo                                                                                        | Uma segunda opinião sobre o seu Odoo                                                                                      |
| We review another supplier's proposal, or audit an Odoo somebody else implemented. No commitment to change anything. | Revisamos a proposta de outro fornecedor, ou auditamos um Odoo que outra pessoa implantou. Sem compromisso de mudar nada. |

Includes the partnership diagnostic checklist, which is the sharpest content on the
page: does your partner run code review, do you receive the source, do they contribute
upstream, can you deploy without them.

## `/academia` — Escodoo Academy

New. The offer exists on the home page today with nowhere to go. Training for
developers, functional consultants and operational teams, with the course catalogue
linking to `/slides`, which is already live.
