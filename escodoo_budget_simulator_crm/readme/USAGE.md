This guide explains how to use the Escodoo Budget Simulator CRM integration to create budget simulations from CRM opportunities.

## Creating a Budget Simulation from an Opportunity

**Method 1: Opportunity with Partner**

If the opportunity already has a partner assigned:

1. Open the CRM opportunity
2. Click the **Create Budget Simulation** button in the header
3. The simulation is created immediately with:
   * Partner automatically populated from the opportunity
   * Opportunity automatically linked
   * Description copied from the opportunity (if available)
4. The simulation form opens automatically
5. Continue with the normal simulation workflow:
   * Load from template (optional)
   * Add modules, integrations, and lines
   * Adjust complexity, users, and companies
   * Recalculate and confirm

**Method 2: Opportunity without Partner**

If the opportunity doesn't have a partner:

1. Open the CRM opportunity
2. Click the **Create Budget Simulation** button in the header
3. A wizard opens with two options:
   * **Create a new customer**: Creates a new partner from the opportunity data
   * **Link to an existing customer**: Allows selecting an existing partner
4. Select the desired option:
   * If "Create a new customer": The partner is created and linked to the opportunity
   * If "Link to an existing customer": Select a partner from the dropdown
5. Click **Confirm**
6. The simulation is created with:
   * Partner populated (new or selected)
   * Opportunity automatically linked
   * Description copied from the opportunity (if available)
7. The simulation form opens automatically
8. Continue with the normal simulation workflow

## Viewing Simulations Linked to an Opportunity

1. Open the CRM opportunity
2. Click the **Simulations Count** button (shows the number of linked simulations)
3. A filtered list of all simulations linked to this opportunity opens
4. You can:
   * View existing simulations
   * Create new simulations (with opportunity pre-filled)
   * Access any simulation directly

## Working with Linked Simulations

When a simulation is linked to an opportunity:

* The **Opportunity** field appears in the General Information section
* The field shows the linked opportunity
* The field is read-only in confirmed, quotation, and cancelled states
* You can search and filter simulations by opportunity

## Creating Sale Orders from Linked Simulations

When creating a sale order from a simulation that has an opportunity:

1. Confirm the simulation (if not already confirmed)
2. Click **Create Quotation** button
3. The sale order is created with:
   * All simulation lines converted to order lines
   * Opportunity automatically linked to the sale order
   * Partner from the simulation
4. The sale order opens automatically
5. The opportunity now shows the linked sale order

**Note**: The opportunity linking uses the `sale_crm` module's functionality, so the sale order will appear in the opportunity's "Quotations" section.

## Workflow Example

1. **Sales team creates opportunity**:
   * Lead is converted to opportunity
   * Opportunity details are filled in

2. **Create budget simulation**:
   * From opportunity, click "Create Budget Simulation"
   * Handle partner if needed (create or link)
   * Simulation opens with opportunity linked

3. **Build the simulation**:
   * Load from template or build from scratch
   * Add modules, integrations, and lines
   * Adjust complexity, users, companies
   * Recalculate and confirm

4. **Create quotation**:
   * From confirmed simulation, click "Create Quotation"
   * Sale order is created and linked to opportunity
   * Opportunity now shows the quotation

5. **Track progress**:
   * View all simulations from the opportunity
   * See the linked sale order in the opportunity
   * Maintain full traceability

## Tips

* Always create simulations from opportunities to maintain the link
* Use the opportunity's description to provide context for the simulation
* The partner selected in the wizard is also linked to the opportunity
* All simulations for an opportunity can be viewed from the opportunity form
* Sale orders created from simulations are automatically linked to opportunities
* Use the opportunity field in simulation search to filter by opportunity
* The integration works seamlessly with the existing Budget Simulator workflow
