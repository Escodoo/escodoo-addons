This guide explains how to use the Escodoo Budget Simulator module to create and manage budget simulations for Odoo implementation projects.

## Creating a Budget Simulation

**Method 1: From Template**

1. Go to **Budget Simulator > Budget Simulations**
2. Click **Create**
3. Fill in the basic information:
   * **Partner**: Select the customer
   * **Template**: Select a template (optional but recommended)
4. Click **Load from Template** button
   * A confirmation dialog will appear warning that all current data will be replaced
   * Click **Continue** to load template data
5. The simulation will be populated with:
   * Modules from the template
   * Integrations from the template
   * General activities from the template
   * Default complexity, users, and companies (if set in template)
6. Adjust the simulation as needed:
   * Modify hours for modules/integrations
   * Add or remove modules/integrations
   * Add custom general activities
   * Adjust complexity, users, or companies
7. Click **Recalculate** to update totals based on current factors
8. Review and click **Confirm** to finalize (moves to "Confirmed" state)

**Method 2: From Scratch**

1. Go to **Budget Simulator > Budget Simulations**
2. Click **Create**
3. Fill in the basic information:
   * **Partner**: Select the customer
   * **Complexity**: Select Low, Medium, or High
   * **Number of Users**: Enter the expected number of users
   * **Number of Companies**: Enter the number of companies/CNPJs
4. Go to the **Modules** tab and add modules:
   * Click **Add a line**
   * Select a module from the catalog
   * Adjust hours if needed (default hours come from catalog)
5. Go to the **Integrations** tab and add integrations:
   * Click **Add a line**
   * Select an integration from the catalog
   * Adjust hours if needed
6. Go to the **General Activities** tab and add activities:
   * Click **Add a line**
   * Select an activitie from the catalog (recommended) or create a custom one
   * If selecting from catalog: name, category, default hours, and description are auto-populated
   * If creating custom: enter name, select category, enter default hours, and add description
   * Adjust hours if needed using the Adjusted Hours field
7. Click **Recalculate** to update totals
8. Review and click **Confirm** to finalize (moves to "Confirmed" state)

## Understanding the Three Types of Lines

**Modules**
* Represent Odoo modules that will be implemented (e.g., Sales, Inventory, Accounting)
* Hours represent the technical implementation effort (configuration, parameterization, testing)
* Selected from a catalog with predefined default hours
* Can be adjusted per simulation

**Integrations**
* Represent external integrations (e.g., NFe, NFS-e, CNAB Receivables, CNAB Payables)
* Hours represent the integration implementation effort
* Selected from a catalog with predefined default hours
* Can be adjusted per simulation

**General Activities**
* Represent specific activities that are not part of standard module/integration implementation
* Can be selected from a catalog or created custom for each simulation
* Categories include:
  * **Discovery**: Analysis, requirements gathering, process mapping
  * **Configuration**: Custom configuration work
  * **Development**: Custom development
  * **Migration**: Data migration activities
  * **Training**: User training sessions
  * **Support**: Support activities
  * **Other**: Any other activity
* When selected from catalog, name, category, default hours, and description are auto-populated
* Hours can be adjusted using the Adjusted Hours field

## Automatic Calculations

The system automatically applies three factors to calculate `final_hours` for each activitie:

1. **Complexity Factor**:
   * Low: 1.00x (no increase)
   * Medium: 1.15x (+15%)
   * High: 1.30x (+30%)

2. **Users Factor**:
   * +1% per user above 5
   * Maximum: +40%
   * Example: 15 users = 1.0 + (15-5) × 0.01 = 1.10x (+10%)

3. **Companies Factor**:
   * +15% per company above 1
   * No maximum limit
   * Example: 3 companies = 1.0 + (3-1) × 0.15 = 1.30x (+30%)

**Formula**: `final_hours = base_hours × complexity_factor × users_factor × company_factor`

All factors are applied at the activitie level, ensuring that:
* Each module, integration, and activitie shows its final calculated hours
* The total hours is simply the sum of all final_hours
* There's no discrepancy between individual activitie totals and the simulation total

## Workflow States

**Draft**
* Initial state when creating a simulation
* All fields can be edited
* Can load from template, recalculate, and make adjustments
* Can confirm to move to "Confirmed" state

**Confirmed**
* Simulation is finalized
* Fields are read-only
* Cannot be reset to Draft
* Can create sales quotation from this state

## Creating Sales Quotations

Once a simulation is in "Confirmed" state:

1. Open the confirmed simulation
2. Click **Create Quotation** button
3. The system will:
   * Create a new sales order
   * Create one line for each module (with description)
   * Create one line for each integration (with description)
   * Create one line for each general activitie (with description)
   * Use the configured default product (or create a generic service product)
   * Set quantities based on final_hours
4. The sales order will open automatically
5. You can now adjust prices, add discounts, and finalize the quotation

**Note**: The default product for quotations can be configured in **Settings > Escodoo Budget Simulator > Default Product for Quotations**

## Generating Reports

1. Open a simulation (any state)
2. Click **Print** button (or use the Print menu)
3. Select **Budget Simulation Report**
4. A PDF will be generated with:
   * Simulation information
   * List of modules with hours
   * List of integrations with hours
   * List of general activities with hours
   * Total hours summary

## Creating a Template

1. Go to **Budget Simulator > Budget Templates**
2. Click **Create**
3. Fill in:
   * **Name**: Template name
   * **Description**: Template description
   * **Default Complexity**: Optional default complexity level
   * **Default Users**: Optional default number of users
   * **Default Companies**: Optional default number of companies
4. Go to **Modules** tab and add modules:
   * Select modules from catalog
   * Adjust hours if needed (these will be used as adjusted_hours in simulations)
5. Go to **Integrations** tab and add integrations:
   * Select integrations from catalog
   * Adjust hours if needed
6. Go to **Lines** tab and add standard activities:
   * Select activities from catalog (recommended) or create custom ones
   * If selecting from catalog: name, category, default hours, and description are auto-populated
   * If creating custom: enter name, select category, enter default hours, and add description
   * Adjust hours if needed using the Adjusted Hours field
7. Save the template

## Using Templates

Templates can be loaded into simulations using the **Load from Template** button. This will:
* Replace all existing modules, integrations, and lines
* Load default values (complexity, users, companies) if set
* Load adjusted hours from template if defined
* Preserve the simulation's partner and other basic information

## Module Catalog

1. Go to **Budget Simulator > Configuration > Modules**
2. Create or edit modules:
   * **Name**: Display name
   * **Code**: Odoo module code (e.g., sale, stock)
   * **Default Hours**: Default implementation hours for this module

## Integration Catalog

1. Go to **Budget Simulator > Configuration > Integrations**
2. Create or edit integrations:
   * **Name**: Display name
   * **Code**: Unique code (e.g., nfe, nfse, cte, mdfe, cnab_receivable)
   * **Default Hours**: Default implementation hours for this integration
   * **Description**: Detailed description of the integration

## General Activitie Catalog

1. Go to **Budget Simulator > Configuration > General Activitie Catalog**
2. Create or edit budget activities:
   * **Name**: Display name
   * **Code**: Unique code (e.g., discovery_analysis, user_training)
   * **Category**: Select category (Discovery, Configuration, Development, Migration, Training, Support, Other)
   * **Default Hours**: Default hours for this activity
   * **Description**: Detailed description of the activity

## Tips

* Use templates to standardize common implementation scenarios
* Adjust hours per simulation when project specifics differ from defaults
* Use general activities for tasks that don't fit standard modules/integrations
* The recalculation button updates totals when you change complexity, users, or companies
* All factors are applied at the activitie level, so individual activitie totals match the simulation total
* Create sales quotations only from confirmed simulations
* Configure the default product in settings to ensure consistent quotation generation

