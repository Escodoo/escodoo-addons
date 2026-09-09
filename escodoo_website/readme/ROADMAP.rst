* Public implementation budget simulator. The estimation engine already exists
  in ``escodoo_budget_simulator``, with module and integration catalogues and
  the complexity, user and company factors. It lacks a front end and a monetary
  price, since it currently produces hours that become a quotation line. An
  ``escodoo_website_budget_simulator`` addon would reuse those models together
  with ``escodoo.website.feature``.
* Total cost simulator comparing Community plus OCA against Enterprise in
  Brazilian reais. ``/investimento`` states the comparison structure today.
* Lead qualification bridge. The form fields for company size, current system,
  number of users and revenue band map onto the ideal customer profile fields
  that already exist in ``escodoo_crm_custom``, which carries scoring,
  classification and the budget gap. Kept in a separate addon so this module
  does not inherit the fiscal lookup dependency.
* Odoo health diagnostic, taking the installed module list and returning how
  many are standard, how many come from the community and how many are
  proprietary custom, with an upgrade risk score.
* English version of the site for the international service lines, as a second
  website record.
* ``escodoo_website_elearning``, extending the Academy pages over the course
  catalogue.
