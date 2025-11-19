This module provides integration between the Escodoo Budget Simulator and CRM Opportunities, allowing sales teams to create budget simulations directly from CRM opportunities and link them throughout the sales process.

## Main Features

* **Create Simulations from Opportunities**: Create budget simulations directly from CRM opportunities with a single click
* **Partner Management**: Wizard to handle partner assignment when creating simulations from opportunities without a partner
* **Automatic Linking**: Automatically link opportunities to simulations and sale orders
* **Opportunity Tracking**: View all budget simulations linked to an opportunity from the opportunity form
* **Sales Order Integration**: When creating a sale order from a simulation, automatically link it to the associated opportunity

## Benefits

* Streamline the sales process by creating budgets directly from opportunities
* Maintain traceability between opportunities, simulations, and sale orders
* Reduce manual data entry by automatically populating partner information
* Track all budget simulations related to an opportunity in one place
* Seamless integration with the existing CRM workflow

## Dependencies

This module requires:
* `escodoo_budget_simulator`: The base Budget Simulator module
* `crm`: CRM module for opportunities management
* `sale_crm`: Integration between Sales and CRM modules

## Workflow

1. Sales team creates or works with a CRM opportunity
2. From the opportunity, click "Create Budget Simulation"
3. If the opportunity has a partner, the simulation is created immediately
4. If the opportunity doesn't have a partner, a wizard opens to:
   * Create a new customer from the opportunity data
   * Link to an existing customer
5. The simulation is created and linked to the opportunity
6. When creating a sale order from the simulation, it's automatically linked to the opportunity
7. All simulations linked to an opportunity can be viewed from the opportunity form
