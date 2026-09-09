# Industry pages

Seven URLs, all kept. This is the largest block of content on the site and also the one
with the largest gap: seven bottom of funnel pages without a single piece of evidence.

## What is preserved

The pain first structure works and stays. The rhetorical pattern is consistent and
effective: concrete operational pain, then the invisible cost in the margin, then the
structure in Odoo, then predictability. The declared antagonist is always the same —
spreadsheets, chat messages, disconnected systems and improvisation. The copy speaks
manager, not IT. The humour stays.

## What changes

### 1. Named modules, from a single source

The manufacturing page today talks about production planning without ever naming the
multi level planning module; the repair page describes repairs without naming RMA or
repair; the field service page describes worksheets without naming field service. The
site holds exactly that information in the feature map and keeps it disconnected from
the pages that need it.

Each industry page now pulls its rows from `escodoo.website.feature` filtered by
`segment_ids`, so the module names come from the same record set that feeds the feature
map and the edition comparison. One source, three renderings.

### 2. Evidence

Each page carries a mini case with numbers, anonymous but real, and the typical KPIs for
the segment. Three full cases exist in `/cases`; the remaining pages reference the
closest one.

### 3. A conversion ladder

Today there is only "talk now". A reader who is still researching and does not want a
conversation has no option. Every page gains the intermediate step:

| EN                                              | PT                                            |
| ----------------------------------------------- | --------------------------------------------- |
| See what Odoo already covers for this operation | Veja o que o Odoo já cobre para esta operação |
| Free 30 minute diagnostic                       | Diagnóstico gratuito de 30 min                |

### 4. Disambiguation between the overlapping four

Maintenance, repair centres, field service and professional services share almost
interchangeable blocks. One sentence about missing parts delaying work and excess parts
trapping capital appears literally on two of them. Rather than merging the URLs and
losing four positions in search, each page opens with an explicit statement of who it is
for and cross links the neighbouring three.

| Page                                   | EN "this page is for"                                          | PT                                                          |
| -------------------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------- |
| `/odoo-erp-para-manutencao`            | Your team maintains assets on a plan, yours or your client's.  | Sua equipe mantém ativos em plano, seus ou do seu cliente.  |
| `/odoo-erp-para-assistencia-tecnica`   | Equipment arrives at your bench, gets diagnosed and goes back. | O equipamento chega à sua bancada, é diagnosticado e volta. |
| `/odoo-erp-para-servico-de-campo`      | Your team travels to the client to execute.                    | Sua equipe se desloca até o cliente para executar.          |
| `/odoo-erp-para-prestacao-de-servicos` | You sell hours, projects or contracts, not equipment.          | Você vende horas, projetos ou contratos, não equipamento.   |

## Page by page

Headlines keep the search wording that already performs, varying between "sistema ERP
para X", "software de gestão" and "sistema de gestão".

| URL                                      | EN headline                        | PT headline                      | Blocks                                                                                                          |
| ---------------------------------------- | ---------------------------------- | -------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `/odoo-erp-para-manufatura`              | ERP for industry and manufacturing | ERP para indústria e manufatura  | Production planning, stock and supply, quality and traceability, industrial maintenance, cost and indicators    |
| `/odoo-erp-para-comercio-e-distribuicao` | ERP for trade and distribution     | ERP para comércio e distribuição | Commercial management, stock and warehouses, purchasing, logistics and picking, recurrence, turnover indicators |
| `/odoo-erp-para-prestacao-de-servicos`   | ERP for service companies          | ERP para empresas de serviços    | Commercial and contracts, tickets and work orders, team and capacity, indicators                                |
| `/odoo-erp-para-servico-de-campo`        | ERP for field service              | ERP para serviço de campo        | Scheduling, field execution, routing, worksheets and evidence, time materials and billing                       |
| `/odoo-erp-para-manutencao`              | ERP for maintenance                | ERP para manutenção              | Preventive and corrective, assets and history, work orders, parts, contracts and SLA, billing                   |
| `/odoo-erp-para-assistencia-tecnica`     | ERP for repair centres             | ERP para assistência técnica     | Intake and triage, diagnosis and repair, parts, bench collection and field, SLA and warranty, billing           |
| `/odoo-erp-para-gestao-de-projetos`      | ERP for project management         | ERP para gestão de projetos      | Planning, execution, team allocation, timesheet cost and billing, indicators                                    |

The professional services page is the thinnest on the live site with only four blocks;
it gains the missing contract and renewal block.

## Closing block

The line that closes every industry page today is the best sentence in the whole set and
stays exactly as it is:

| EN                                                                 | PT                                                              |
| ------------------------------------------------------------------ | --------------------------------------------------------------- |
| We do not just deliver screens and forms. We structure operations. | Não entregamos apenas telas e cadastros. Estruturamos operação. |
