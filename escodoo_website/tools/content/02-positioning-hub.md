# Positioning hub — Community + OCA

This is the cluster that carries the thesis. Everything else on the site links into it.

## Home — `/`

| Block              | EN                                                                                                         | PT                                                                                                   |
| ------------------ | ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Hero headline      | The Odoo you control                                                                                       | O Odoo que você controla                                                                             |
| Hero subheadline   | Community + OCA is not the cheap Odoo. It is the edition whose code you can read, audit and take with you. | Community + OCA não é o Odoo barato. É a edição cujo código você pode ler, auditar e levar com você. |
| Hero primary CTA   | Talk to a specialist                                                                                       | Falar com especialista                                                                               |
| Hero secondary CTA | Free 30 minute diagnostic                                                                                  | Diagnóstico gratuito de 30 min                                                                       |
| Proof strip        | We reviewed 794 community contributions in 2025                                                            | Revisamos 794 contribuições da comunidade em 2025                                                    |
| Proof strip detail | The code that reaches your ERP passed through us before it became standard.                                | O código que chega ao seu ERP passou por nós antes de virar padrão.                                  |
| Seal               | Two of our engineers among the twenty largest OCA contributors worldwide                                   | Dois de nossos engenheiros entre os vinte maiores contribuidores da OCA no mundo                     |
| Seal link          | Check the public ranking                                                                                   | Confira o ranking público                                                                            |

Sections in order: hero, proof strip with the verifiable seal, the three column edition
teaser, solutions by pain, services, industries, an anonymous case with numbers, the tax
reform strip, and the closing double CTA.

The tax reform strip exists because Brazilian buyers now expect it on the home page —
both large local incumbents put it there.

## Editions — `/edicoes-odoo`

The decisive change is a **third column**. The widely read comparison published by the
largest Odoo partner compares Community **without OCA** against Enterprise and marks
Enterprise as recommended, which makes Community lose almost every row. Adding the
middle column is the whole argument.

| Column | EN header             | PT header          |
| ------ | --------------------- | ------------------ |
| 1      | Community, on its own | Community, sozinho |
| 2      | Community + OCA       | Community + OCA    |
| 3      | Enterprise            | Enterprise         |

Rendered from `escodoo.website.feature`, so the rows cite the OCA module by name and
link its repository instead of asserting parity.

Honesty block, which is what makes the rest credible:

| EN                                                                                                                                                                                          | PT                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Choose Enterprise when you need Odoo Studio, the native mobile app, a support agreement signed by Odoo S.A. or the newest assisted features. We will tell you so, and we will implement it. | Escolha Enterprise quando você precisa do Odoo Studio, do app mobile nativo, de um contrato de suporte assinado pela Odoo S.A. ou dos recursos assistidos mais recentes. Nós vamos dizer isso, e vamos implementar. |
| Choose Community + OCA when the code that runs your operation has to be readable, auditable and portable between suppliers.                                                                 | Escolha Community + OCA quando o código que roda sua operação precisa ser legível, auditável e portável entre fornecedores.                                                                                         |

Closing CTA is a conversion CTA, not a navigation link. The live page ends with
"understand Odoo better", which asks nothing of a reader who has just made a decision.

## Our contribution to the OCA — `/oca`

The current page explains the OCA as an institution and never says what Escodoo does
inside it. The focus inverts.

| Block                | EN                                                                                                                                                | PT                                                                                                                                                              |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Headline             | What we do inside the OCA                                                                                                                         | O que fazemos dentro da OCA                                                                                                                                     |
| Subheadline          | Not how much code we write. How much of the community's code we review before it becomes standard.                                                | Não quanto código escrevemos. Quanto do código da comunidade revisamos antes de virar padrão.                                                                   |
| Ranking block        | Rank 9 worldwide in the 2025 OCA contributor index                                                                                                | 9º lugar mundial no índice de contribuição da OCA em 2025                                                                                                       |
| Ranking link label   | Open the public dataset                                                                                                                           | Abrir o dataset público                                                                                                                                         |
| Translation to value | Every module we push upstream is a module you do not pay to maintain, that survives upgrades, and that does not depend on Escodoo still existing. | Cada módulo que levamos para o upstream é um módulo que você não paga para manter, que sobrevive a upgrades e que não depende de a Escodoo continuar existindo. |

That last pair is the bridge that turns a contribution claim into an economic argument.
Without it, "we are top ten" is vanity.

Also on the page: the maintained modules with links, the team members with their GitHub
handles, and a short explanation of what the OCA is — reduced to a supporting role
rather than being the subject.

## Feature map — `/mapa-de-funcionalidades`

Content is preserved; it is the best asset on the site and the level of detail is
unusual for the category. Three changes:

1. Rendered from `escodoo.website.feature`, so it stops being duplicated markup across
   three URLs and the search stops serving an empty state.
2. Every row is versioned, and rows resolved by the community cite the module.
3. It finally asks for something: a lead capture offering the map as a PDF.

| EN                                   | PT                                   |
| ------------------------------------ | ------------------------------------ |
| Get the full map as a PDF            | Receba o mapa completo em PDF        |
| Which of these do you actually need? | Quais destes você realmente precisa? |

Qualitative badges become explicit levels so they are comparable: `Not covered` /
`Não atendido`, `Partially covered` / `Atendido parcialmente`, `Fully covered` /
`Atendido`.

## Investment — `/investimento`

The company's central differentiator is economic and the live site never shows a
calculation. This page does not publish an implementation price list. It publishes the
three things that reduce anxiety without giving away margin.

| Block          | EN                                                                                                                                                                                           | PT                                                                                                                                                                                              |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Headline       | What an Odoo project costs, and how we price it                                                                                                                                              | Quanto custa um projeto Odoo, e como cobramos                                                                                                                                                   |
| Ranges         | Ranges per productised service line                                                                                                                                                          | Faixas por linha de serviço produtizada                                                                                                                                                         |
| Contract model | Time and materials or fixed scope, and when each applies                                                                                                                                     | Escopo aberto ou fechado, e quando cada um se aplica                                                                                                                                            |
| Benchmark      | Comparable companies invest around one percent of annual revenue in their management platform, and reserve fifteen to twenty five percent of the implementation cost per year for evolution. | Empresas comparáveis investem cerca de um por cento do faturamento anual na plataforma de gestão, e reservam de quinze a vinte e cinco por cento do custo de implantação por ano para evolução. |

It also carries the honest side of the Community argument: zero licensing does not mean
zero cost, because Community trades licence fees for service. Saying this first is what
makes the rest believable.

The interactive total cost simulator is roadmap, not this phase. The page states the
comparison structure and links the diagnostic instead.

## Sovereignty and portability — `/soberania-e-portabilidade`

The page that disarms the larger buyer's objections, none of which the live site
addresses.

Blocks: who owns the code, the repository handed to the client, LGPD and data residency,
what happens if Escodoo leaves the project, how to move to another supplier, and
references for due diligence.

| EN                                                                                           | PT                                                                                           |
| -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Changing supplier should be a commercial decision, not a technical drama.                    | Trocar de fornecedor deve ser uma decisão comercial, não um drama técnico.                   |
| You get the source, the repository and the deployment recipe. Leaving is possible by design. | Você recebe o código, o repositório e a receita de implantação. Sair é possível por desenho. |

## What Odoo is — `/odoo`

Kept as the "what is Odoo" pillar, with the embedded full feature map removed — it
duplicated an entire URL — and the repeated implementation block removed too. The market
positioning quadrant stays; it is the only competitor comparison on the site and it is a
strong visual asset. Its truncated labels get fixed.

## Odoo in Brazil — `/odoo-brasil`

Kept as the localisation and fiscal pillar. Two fixes:

- One single, defensible position on Brazilian fiscal coverage. Today the feature map
  says NF-e is complete and mature while the FAQ says fiscal requirements are not part
  of the core and may need integration with an external fiscal product. A lead comparing
  both finds contradictory messages on the most critical point in this market.
- The four step method is removed. The same process is described in six steps on the
  implementation page and in seven in the FAQ. One description, one place.

The best paragraph on the current site is preserved almost verbatim, because it is the
sentence that separates Escodoo from integrators who only consume OCA:

| EN                                       | PT                               |
| ---------------------------------------- | -------------------------------- |
| We contribute, we do not merely consume. | Contribuir, não apenas consumir. |

## Who should run your project — `/freelancer-odoo-ou-empresa-especializada`

Good page, good format, kept. Two upgrades:

1. The table is substantiated. "Complete team" becomes a number, "high fiscal
   experience" becomes something checkable.
2. The axis is widened. Today only freelancer versus firm exists. The market also
   compares against an official Odoo partner and against a traditional local ERP
   consultancy, and the quote form already proves the migration demand arrives.

Added criteria, which are the checkable and decisive ones the page lacks: contract and
invoicing, cover during holidays or illness, who owns the code, whether the repository
is handed over, and what happens if the supplier disappears mid go live.
