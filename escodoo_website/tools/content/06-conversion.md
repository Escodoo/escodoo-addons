# Conversion layer

## The problem being fixed

The live site asks for exactly two things: talk to us, or fill in a long form. There is
nothing for a reader who is still researching. Three forms have partially overlapping
purposes with no visible logic for which to use when — the FAQ tries to solve it by
listing four channels by demand type, which is a symptom of confused architecture rather
than a solution.

## Two speeds, everywhere

Every page carries the same pair, in this order.

| Role            | EN                        | PT                             | Target                  |
| --------------- | ------------------------- | ------------------------------ | ----------------------- |
| High commitment | Talk to a specialist      | Falar com especialista         | `/contactus`            |
| Low commitment  | Free 30 minute diagnostic | Diagnóstico gratuito de 30 min | `/diagnostico-gratuito` |

## `/diagnostico-gratuito` — the low friction entry

New. Five fields, no company registration number, no revenue.

Fields: name, corporate email, company, current situation as a select, and optional
phone.

The current situation select is what routes the lead, and its options map the solution
pages:

| EN option                    | PT option                                         |
| ---------------------------- | ------------------------------------------------- |
| We are evaluating Odoo       | Estamos avaliando o Odoo                          |
| We use Odoo and need support | Usamos Odoo e precisamos de suporte               |
| Our Odoo project stalled     | Nosso projeto de Odoo travou                      |
| We want to leave another ERP | Queremos sair de outro ERP                        |
| We need to upgrade version   | Precisamos migrar de versão                       |
| We need tax reform readiness | Precisamos nos preparar para a Reforma Tributária |

## `/contactus` — qualified contact

Rewrite, replacing the core view. Today it is the stock Odoo form with an English page
title in an otherwise Portuguese site, no qualification, no response promise, no
business hours and no explicit link to messaging.

Added: a minimum qualification, a stated response time, the full company details, and a
trust block beside the form. The stock form has none of these.

| EN                                                                                        | PT                                                                                     |
| ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| We answer within one business day.                                                        | Respondemos em até um dia útil.                                                        |
| We do not share your data, and we will not add you to a mailing list you did not ask for. | Não compartilhamos seus dados, e não vamos te incluir em uma lista que você não pediu. |

## `/solicitacao-de-orcamento` — quote request

Kept; it is the best form on the site and already qualifies company size, project type
and job title. The option for migrating an existing ERP shows competitive awareness and
stays.

Fixes: the company registration number becomes optional, because requiring it on a first
contact excludes anyone still researching. Number of users and desired timeline are
added, since the FAQ itself says those are the fields that speed up a proposal. A trust
block goes beside the form. The `Whatsapp` heading is removed and the confusing headline
about security is corrected.

## `/acesso-ao-ambiente-de-demonstracao` — demo access

Rewrite. This is the highest intent page on the site and the largest conversion loss.
Today it promises an immediate trial, asks for twelve fields including annual revenue,
delivers a request for access, and ships a typo in its main button.

Changes: five fields, no revenue, an honest promise, and an explanation of what the
visitor will actually see — the module scope of the environment, whether the fiscal
localisation is included, how long the access lasts, and a video for whoever does not
want to fill in anything. The internal field labels leaking into the public page are
removed.

| EN                                                            | PT                                                                 |
| ------------------------------------------------------------- | ------------------------------------------------------------------ |
| Guided demo of Odoo Community with the Brazilian localisation | Demonstração guiada do Odoo Community com a localização brasileira |
| Prefer to just watch? See the recorded tour.                  | Prefere apenas assistir? Veja o tour gravado.                      |

The remaining `/solicitacao-de-*` pages keep their URLs and their purpose, with the same
trust block and the corrected headings.

## Lead routing

Every form creates a `crm.lead`. Routing happens through hidden fields resolved at
install time, following the pattern already used elsewhere in the group's website addons
— placeholders in the page XML, replaced in `data/website_theme_apply.xml` so the
identifiers do not have to be guessed.

| Placeholder            | Resolves to                                                                           |
| ---------------------- | ------------------------------------------------------------------------------------- |
| `*crm_team_website*`   | the sales team named for website intake, falling back to the default sales department |
| `*utm_medium_website*` | the website medium                                                                    |
| `*utm_source_<page>*`  | a source per form, so the origin page is visible on the lead                          |

The qualification fields captured by the forms — company size, current system, number of
users, revenue band — map onto the ideal customer profile fields that already exist in
the group's CRM customisation, which carries scoring, classification and the budget gap.
Wiring that mapping is a separate bridge addon so this module does not inherit a fiscal
lookup dependency; it is listed in the roadmap.

## Thank-you pages

Three, all with a next step rather than a dead end.

| URL                                 | Purpose                                |
| ----------------------------------- | -------------------------------------- |
| `/obrigado`                         | generic, used by the request forms     |
| `/contactus-thank-you`              | contact form, states the response time |
| `/mapa-de-funcionalidades/obrigado` | delivers the feature map PDF link      |

| EN                                                                          | PT                                                                                         |
| --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Thank you. Now what happens.                                                | Obrigado. Agora, o que acontece.                                                           |
| While you wait, these are the three pages our clients read before deciding. | Enquanto você espera, estas são as três páginas que nossos clientes leem antes de decidir. |
