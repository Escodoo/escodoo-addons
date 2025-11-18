This guide explains how to configure the Escodoo Budget Simulator module.

## Installation

1. Go to the **Apps** menu
2. Remove the "Apps" filter if necessary
3. Search for "Escodoo Budget Simulator"
4. Click **Install**

The module will automatically install the necessary dependencies:
* `base`
* `contacts`
* `mail`
* `sales_team`
* `sale`

## Set Up Module Catalog

1. Go to **Budget Simulator > Configuration > Modules**
2. Create entries for commonly used Odoo modules:
   * **Name**: Display name (e.g., "Sales", "Inventory")
   * **Code**: Odoo module code (e.g., "sale", "stock")
   * **Default Hours**: Typical implementation hours for this module
   * **Active**: Check to enable the module in selections

**Example Modules**:
* Sales (sale): 20 hours
* Inventory (stock): 25 hours
* Accounting (account): 30 hours
* Brazilian Fiscal (l10n_br_fiscal): 35 hours

## Configure Default Product for Quotations

1. Go to **Settings > Escodoo Budget Simulator**
2. In the **Default Product for Quotations** field:
   * Select a service product that will be used when creating sales orders from simulations
   * This product should be:
     * Type: Service
     * Saleable: Yes
3. Click **Save**

**Note**: If no product is configured, the system will:
1. Search for an existing service product with "hour" in the name
2. If not found, create a generic "Consulting Service (Hours)" product

## Set Up Integration Catalog

1. Go to **Budget Simulator > Configuration > Integrations**
2. Create entries for commonly used integrations:
   * **Name**: Display name (e.g., "NFe", "NFS-e", "CT-e", "MDF-e")
   * **Code**: Unique code (e.g., "nfe", "nfse", "cte", "mdfe", "cnab_receivable")
   * **Default Hours**: Typical implementation hours for this integration
   * **Description**: Detailed description of the integration
   * **Active**: Check to enable the integration in selections

**Example Integrations**:
* NFe: 40 hours
* NFS-e: 30 hours
* CT-e: 45 hours
* MDF-e: 50 hours
* CNAB Receivables: 50 hours
* CNAB Payables: 45 hours
* SPED: 60 hours

## Set Up General Activitie Catalog

1. Go to **Budget Simulator > Configuration > General Activitie Catalog**
2. Create entries for commonly used budget activities:
   * **Name**: Display name (e.g., "Discovery and Requirements Analysis", "User Training")
   * **Code**: Unique code (e.g., "discovery_analysis", "user_training")
   * **Category**: Select category (Discovery, Configuration, Development, Migration, Training, Support, Other)
   * **Default Hours**: Typical hours required for this activity
   * **Description**: Detailed description of the activity
   * **Active**: Check to enable the activitie in selections

**Example Budget Activities**:
* Discovery and Requirements Analysis: 40 hours (Discovery)
* System Configuration: 60 hours (Configuration)
* Custom Development: 80 hours (Development)
* Data Migration: 50 hours (Migration)
* User Training: 30 hours (Training)
* Go-Live Support: 40 hours (Support)

## Create Budget Templates

1. Go to **Budget Simulator > Budget Templates**
2. Create templates for common scenarios:
   * **Standard Implementation**: Basic Odoo with Brazilian fiscal
   * **E-commerce Multi-Company**: Odoo with e-commerce focus and multiple companies
   * **Manufacturing with Transport**: Odoo with manufacturing modules and transport integrations

For each template:
1. Set default values (complexity, users, companies) if applicable
2. Add modules that are typically included
3. Add integrations that are typically required
4. Add standard general activities from catalog or create custom ones
5. Use **Recalculate** button to update totals based on current factors
6. **Confirm** the template to lock it (can be reset to draft if needed)

## User Groups and Permissions

The module creates two user groups:

**Budget User**
* Can view and create budget simulations
* Can view and create templates
* Can view catalogs (modules and integrations)
* Implied by: Internal User

**Budget Manager**
* All Budget User permissions
* Can manage all budget simulations
* Can manage templates
* Can manage catalogs (modules and integrations)
* Automatically includes: Administrator and System users

**Note**: Administrators are automatically added to the Budget Manager group upon module installation.

## Access Rights

The module provides the following access rights:

* **Budget Simulations**: Users can access their own simulations; Managers can access all
* **Budget Templates**: Users can create and edit templates
* **Modules Catalog**: Users can view; Managers can create/edit
* **Integrations Catalog**: Users can view; Managers can create/edit
* **General Activitie Catalog**: Users can view; Managers can create/edit

## Configuration Parameters

The module uses the following configuration parameter:

* `escodoo_budget_simulator.default_quotation_product_id`: Stores the default product ID for creating quotations

This parameter is managed through the Settings interface and does not require manual configuration.

## Sequence Configuration

The module creates a sequence for budget simulations:
* **Code**: `budget.simulation`
* **Prefix**: Auto-generated based on sequence configuration
* **Padding**: Standard Odoo sequence padding

Sequences can be configured in **Settings > Technical > Sequences**.

## Report Configuration

The module includes a QWeb PDF report:
* **Report Name**: Budget Simulation Report
* **Model**: `budget.simulation`
* **Format**: PDF

The report can be customized by modifying the QWeb template in `report/budget_simulation_report.xml`.

## Multi-Company Support

The module supports multi-company environments:
* Each simulation is linked to a company
* Users can only see simulations from their accessible companies
* Company-specific configurations are respected

## Tips

* Start by setting up the module, integration, and general activitie catalogs with your standard offerings
* Create templates for your most common implementation scenarios
* Configure the default product before creating quotations
* Use the demo data as a reference for setting up your catalogs
* Regularly review and update default hours based on actual project experience
* Templates can be confirmed to lock them, but can be reset to draft if changes are needed
* All changes to important fields are tracked in the chatter (mail tracking)

