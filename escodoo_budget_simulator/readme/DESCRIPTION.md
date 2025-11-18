This module allows the Escodoo sales team to simulate project costs for Odoo implementations. It provides a comprehensive budgeting system with templates, automatic calculations, and integration with sales quotations.

## Main Features

* **Budget Templates**: Create reusable templates that pre-populate new simulations with standard configurations
* **Module Catalog**: Maintain a catalog of Odoo modules with default implementation hours
* **Integration Catalog**: Maintain a catalog of integrations (NFe, NFS-e, CNAB, CT-e, MDF-e, etc.) with default hours
* **General Activitie Catalog**: Maintain a catalog of general activities (discovery, configuration, training, etc.) with default hours
* **Budget Simulations**: Create detailed budget simulations with:
  * Module selection from catalog
  * Integration selection from catalog
  * General activities selection from catalog or custom creation
  * Complexity levels (Low, Medium, High)
  * Number of users and companies
  * Automatic calculation of final hours based on factors
* **Automatic Calculations**:
  * Complexity factors (Low: 1.00x, Medium: 1.15x, High: 1.30x)
  * User factors (1% per user above 5, maximum +40%)
  * Company factors (15% per company above 1, no maximum limit)
  * All factors are applied at the activitie level for consistency
* **Workflow Management**: Draft → Confirmed states
* **Sales Integration**: Create sales quotations directly from confirmed simulations
* **PDF Reports**: Generate detailed PDF reports with breakdown of modules, integrations, and lines

## Benefits

* Standardize budget estimation process across projects
* Reuse templates for similar implementations
* Automatically calculate hours based on project complexity and scale
* Track detailed activities separately from module/integration implementation
* Generate professional PDF reports for clients
* Seamlessly convert approved budgets into sales quotations
* Maintain catalogs of modules, integrations, and general activities for consistency
* Track changes with mail tracking on important fields

## Dependencies

This module requires:
* `base`: Odoo base module
* `contacts`: Contact management
* `mail`: Messaging and activities
* `sales_team`: Sales team management
* `sale`: Sales order management

