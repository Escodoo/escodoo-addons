# Information architecture

## Top menu — six entries

| Sequence | EN label             | PT label               | Target                       |
| -------- | -------------------- | ---------------------- | ---------------------------- |
| 20       | Solutions            | Soluções               | dropdown, no page of its own |
| 30       | Services             | Serviços               | dropdown, no page of its own |
| 40       | Industries           | Segmentos              | dropdown, no page of its own |
| 50       | Community + OCA      | Community + OCA        | dropdown, no page of its own |
| 60       | Company              | Empresa                | dropdown, no page of its own |
| 70       | Talk to a specialist | Falar com especialista | `/contactus`                 |

`Blog`, `/slides` (Academia course catalogue), `/jobs` and `/events` stay owned by their
own Odoo apps. The menu links to them; this addon does not manage them.

## Page inventory

Legend for the origin column: `keep` = content survives with fixes only, `rewrite` =
same URL, new copy, `new` = did not exist.

### Solutions — organised by the buyer's pain

| URL                        | Origin          | EN title                             | PT title                       |
| -------------------------- | --------------- | ------------------------------------ | ------------------------------ |
| `/implantacao-odoo`        | rewrite         | Odoo implementation                  | Implantação do Odoo            |
| `/resgate-de-projeto-odoo` | new             | Rescue a failing Odoo project        | Resgate de projeto Odoo        |
| `/migracao-de-versao-odoo` | new (split out) | Odoo version upgrade                 | Migração de versão do Odoo     |
| `/migrar-para-odoo`        | new             | Move from Totvs, SAP or a legacy ERP | Migrar de Totvs, SAP ou legado |
| `/padronizacao-odoo`       | new             | Standardise your customisations      | Padronização de customizações  |
| `/reforma-tributaria-odoo` | new             | Brazilian tax reform readiness       | Reforma Tributária no Odoo     |

### Services

| URL                              | Origin          | EN title                   | PT title                      |
| -------------------------------- | --------------- | -------------------------- | ----------------------------- |
| `/consultoria-e-desenvolvimento` | rewrite         | Consulting and development | Consultoria e desenvolvimento |
| `/manutencao-odoo`               | rewrite         | Support and maintenance    | Suporte e manutenção          |
| `/hospedagem-odoo`               | new (split out) | Hosting and infrastructure | Hospedagem e infraestrutura   |
| `/arquitetura-de-processos`      | keep            | Process architecture       | Arquitetura de processos      |
| `/segunda-opiniao`               | new             | Second opinion             | Segunda opinião               |
| `/academia`                      | new             | Escodoo Academy            | Academia Escodoo              |

### Industries

| URL                                      | Origin  | EN title                       | PT title                         |
| ---------------------------------------- | ------- | ------------------------------ | -------------------------------- |
| `/odoo-erp-para-manufatura`              | rewrite | ERP for manufacturing          | ERP para manufatura              |
| `/odoo-erp-para-comercio-e-distribuicao` | rewrite | ERP for trade and distribution | ERP para comércio e distribuição |
| `/odoo-erp-para-prestacao-de-servicos`   | rewrite | ERP for professional services  | ERP para prestação de serviços   |
| `/odoo-erp-para-servico-de-campo`        | rewrite | ERP for field service          | ERP para serviço de campo        |
| `/odoo-erp-para-manutencao`              | rewrite | ERP for maintenance            | ERP para manutenção              |
| `/odoo-erp-para-assistencia-tecnica`     | rewrite | ERP for repair centres         | ERP para assistência técnica     |
| `/odoo-erp-para-gestao-de-projetos`      | rewrite | ERP for project management     | ERP para gestão de projetos      |

### Community + OCA — the positioning hub

| URL                                         | Origin  | EN title                                 | PT title                                 |
| ------------------------------------------- | ------- | ---------------------------------------- | ---------------------------------------- |
| `/edicoes-odoo`                             | rewrite | Community, Community + OCA or Enterprise | Community, Community + OCA ou Enterprise |
| `/oca`                                      | rewrite | Our contribution to the OCA              | Nossa contribuição para a OCA            |
| `/mapa-de-funcionalidades`                  | keep    | Feature map                              | Mapa de funcionalidades                  |
| `/investimento`                             | new     | Investment and total cost                | Investimento e custo total               |
| `/soberania-e-portabilidade`                | new     | Sovereignty and portability              | Soberania e portabilidade                |
| `/odoo`                                     | rewrite | What Odoo is                             | O que é o Odoo                           |
| `/odoo-brasil`                              | keep    | Odoo in Brazil                           | Odoo no Brasil                           |
| `/freelancer-odoo-ou-empresa-especializada` | keep    | Who should run your project              | Quem deve conduzir seu projeto           |

### Company

| URL                              | Origin  | EN title                    | PT title                        |
| -------------------------------- | ------- | --------------------------- | ------------------------------- |
| `/aboutus`                       | rewrite | About Escodoo               | Sobre a Escodoo                 |
| `/cases`                         | new     | Results                     | Resultados                      |
| `/cases/industria-metalmecanica` | new     | Metalworking industry       | Indústria metalmecânica         |
| `/cases/distribuidora`           | new     | Wholesale distributor       | Distribuidora                   |
| `/cases/servicos-tecnicos`       | new     | Technical services provider | Prestadora de serviços técnicos |
| `/internacional`                 | new     | International services      | Serviços internacionais         |
| `/faq`                           | rewrite | Frequently asked questions  | Perguntas frequentes            |

### Conversion

| URL                                             | Origin  | Purpose                                        |
| ----------------------------------------------- | ------- | ---------------------------------------------- |
| `/contactus`                                    | rewrite | Qualified contact form, replaces the core view |
| `/diagnostico-gratuito`                         | new     | Low friction 30 minute diagnostic              |
| `/solicitacao-de-orcamento`                     | keep    | Implementation quote request                   |
| `/solicitacao-de-consultoria-e-desenvolvimento` | keep    | Consulting request                             |
| `/solicitacao-de-contrato-de-manutencao`        | keep    | Maintenance contract request                   |
| `/solicitacao-de-migracao-e-hospedagem`         | keep    | Migration and hosting request                  |
| `/solicitacao-de-demonstracao`                  | keep    | Demo request                                   |
| `/acesso-ao-ambiente-de-demonstracao`           | rewrite | Trimmed to five fields, honest promise         |
| `/obrigado`                                     | new     | Generic thank-you                              |
| `/contactus-thank-you`                          | new     | Contact thank-you                              |
| `/mapa-de-funcionalidades/obrigado`             | new     | Feature map PDF delivery                       |

Total: 48 routes, of which `/` and `/contactus` replace core views instead of
registering a `website.page`, because the `website` module already owns them.

## URL map and redirects

`website.rewrite` records, all `301`.

| From                                        | To                 | Reason                                                                                                                                                             |
| ------------------------------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `/servicos-de-infraestrutura-e-sustentacao` | `/hospedagem-odoo` | The old URL carried two distinct offers, hosting and version upgrade, competing for the same page. Hosting keeps the traffic; the page links to the upgrade page.  |
| `/sua-jornada-odoo`                         | `/segunda-opiniao` | It duplicated the menu, but opened with the strongest angle on the site: your current partner may not be serving you. That angle becomes the second opinion offer. |
| `/ebook-thank-you`                          | `/obrigado`        | Consolidated thank-you.                                                                                                                                            |

Kept unchanged so the accumulated authority is not lost: `/oca`, `/odoo`,
`/odoo-brasil`, `/edicoes-odoo`, `/mapa-de-funcionalidades`, `/faq`, `/contactus`,
`/aboutus`, `/implantacao-odoo`, `/consultoria-e-desenvolvimento`, `/manutencao-odoo`,
`/arquitetura-de-processos`, the seven industry URLs, the five `/solicitacao-de-*` URLs,
`/acesso-ao-ambiente-de-demonstracao` and `/freelancer-odoo-ou-empresa-especializada`.

## Defects in the live site fixed on the way

Recorded here because they are the reason several pages are marked `rewrite` rather than
`keep`:

- Duplicated `<h1>` on `/implantacao-odoo`, `/consultoria-e-desenvolvimento`,
  `/manutencao-odoo` and `/servicos-de-infraestrutura-e-sustentacao`.
- `/sua-jornada-odoo` has no `<h1>` at all.
- An `<h1>` literally reading `Whatsapp` on `/solicitacao-de-orcamento`.
- English `<title>` on `/contactus` in an otherwise Portuguese site.
- Typos shipped to production: `SOLITAÇÃO` on the demo button, `Raking` in the OCA
  ranking heading, `integração c m` on the implementation page, `Durante Durante` on the
  process architecture page.
- Zero width characters pasted inside button labels, which screen readers read as broken
  words.
- Internal Odoo field labels leaking into the public demo form: `Custom Seleção`,
  `Campanha`.
- The feature comparison widget serving `0 Funcionalidades` and
  `Nenhum resultado encontrado` in its initial state.
- The OCA ranking block on `/oca` renders an empty heading, so the single rarest
  credential the company owns is invisible to readers.
- `/manutencao-odoo` and `/faq` end with a call to action sentence and no button or
  form.
- `/mapa-de-funcionalidades`, the most valuable asset on the site, captures no contact
  detail at all.
