After installing the module the public site is served in Portuguese, with
English kept as the source language of every string.

Main routes:

* ``/`` home, carrying the positioning thesis and the verifiable OCA seal
* ``/edicoes-odoo`` Community, Community + OCA and Enterprise side by side
* ``/oca`` what Escodoo does inside the OCA, with a link to the public ranking
* ``/mapa-de-funcionalidades`` capability assessment per area
* ``/investimento`` price ranges, contract models and cost benchmarks
* ``/soberania-e-portabilidade`` code ownership, data residency and exit plan
* ``/implantacao-odoo``, ``/consultoria-e-desenvolvimento``,
  ``/manutencao-odoo``, ``/hospedagem-odoo``, ``/arquitetura-de-processos``,
  ``/academia``, ``/segunda-opiniao`` service lines
* ``/resgate-de-projeto-odoo``, ``/migracao-de-versao-odoo``,
  ``/migrar-para-odoo``, ``/padronizacao-odoo``, ``/reforma-tributaria-odoo``
  solutions by situation
* ``/odoo-erp-para-*`` seven industry pages
* ``/cases`` anonymous results
* ``/internacional`` service lines offered outside Brazil
* ``/contactus``, ``/diagnostico-gratuito`` and the ``/solicitacao-de-*`` forms

Every page is a regular website builder page, so the content can be edited from
the front end with **Edit**.

Feature map
~~~~~~~~~~~

The assessment is maintained in the back end under **Website → Configuration →
Feature Map**. Each record states the coverage by Community on its own, by
Community combined with the OCA ecosystem and by Enterprise, plus the modules
that close the gap and the Odoo version the assessment refers to.

Tagging a feature with a segment makes it appear on the matching industry page,
which is what keeps the industry copy and the feature map from drifting apart.

``/mapa-de-funcionalidades/pdf`` renders the same records as a PDF, which is
what the lead capture on the feature map page delivers.

Forms
~~~~~

Every form creates a ``crm.lead`` through the shared ``short_lead_form``
template. The sales team, the medium and the source are resolved when the page
renders, in ``website.escodoo_lead_defaults``, so one template serves every
page and the lead still records which page produced it.

Images
~~~~~~

To refresh the pictures from the live site, run ``tools/download_assets.sh``
from the module directory. It downloads and optimises every image into
``static/src/binary/ir_attachment/``, which is what
``data/ir_attachment_pre.xml`` loads. Run ``tools/build_attachment_xml.py``
afterwards to regenerate that file.

Copy and translation
~~~~~~~~~~~~~~~~~~~~

``tools/content/`` holds the authoring source of truth for the copy, page by
page. It is not loaded by Odoo.

The Portuguese translation is authored in ``tools/i18n/pt_BR/*.json`` as a
mapping of source string to translation, and ``tools/i18n/build_po.py`` turns
those files plus the exported template into ``i18n/pt_BR.po``. Run it with
``--check`` to report coverage without writing:

.. code-block:: shell

   python3 tools/i18n/build_po.py --check
   python3 tools/i18n/build_po.py
