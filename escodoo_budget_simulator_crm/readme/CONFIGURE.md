This guide explains how to configure the Escodoo Budget Simulator CRM integration module.

## Installation

1. Ensure that the base module `escodoo_budget_simulator` is installed
2. Ensure that the `crm` and `sale_crm` modules are installed
3. Go to the **Apps** menu
4. Remove the "Apps" filter if necessary
5. Search for "Escodoo Budget Simulator CRM"
6. Click **Install**

The module will automatically install the necessary dependencies:
* `escodoo_budget_simulator` (base Budget Simulator module)
* `crm` (CRM module)
* `sale_crm` (Sales-CRM integration)

## No Additional Configuration Required

This module extends the functionality of the Budget Simulator and CRM modules without requiring additional configuration. Once installed, the integration features are immediately available:

* **Create Budget Simulation** button appears on CRM opportunity forms
* **Simulations Count** button shows the number of linked simulations
* **Opportunity** field is available in budget simulation forms
* Automatic linking between opportunities, simulations, and sale orders

## Access Rights

The module uses the same access rights as the base Budget Simulator module:

* **Budget User**: Can create simulations from opportunities
* **Budget Manager**: Full access to all simulation features

CRM access rights apply normally:
* Users can access opportunities based on their CRM permissions
* Sales team members can create simulations from their opportunities

## Integration Points

The module adds the following integration points:

1. **CRM Opportunity Form**:
   * "Create Budget Simulation" button in the header
   * "Simulations Count" statistical button showing linked simulations
   * "View Simulations" action to see all linked simulations

2. **Budget Simulation Form**:
   * "Opportunity" field in the General Information section
   * Field is automatically populated when creating from an opportunity
   * Field is read-only in confirmed, quotation, and cancelled states

3. **Wizard for Partner Selection**:
   * Opens when creating a simulation from an opportunity without a partner
   * Options to create a new customer or link to an existing one
   * Ensures the simulation always has a valid partner

4. **Sale Order Creation**:
   * When creating a sale order from a simulation with an opportunity
   * The sale order is automatically linked to the opportunity
   * Uses the `sale_crm` module's opportunity linking functionality

## Tips

* The integration works seamlessly with the existing Budget Simulator workflow
* Simulations created from opportunities maintain the link throughout the sales process
* Use the opportunity's description field to provide context for the simulation
* The partner selected in the wizard is also linked to the opportunity (if using "Create" or "Link" options)
* All simulations linked to an opportunity can be viewed from the opportunity's "View Simulations" button
