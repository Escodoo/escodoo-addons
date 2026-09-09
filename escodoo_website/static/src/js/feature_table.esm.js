/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.EscodooFeatureTable = publicWidget.Widget.extend({
    selector: "[data-escodoo-feature-table]",
    events: {
        input: "_onSearchInput",
    },

    start() {
        this.searchInput = this.el.querySelector(".escodoo-feature-search");
        this.emptyMessage = this.el.querySelector(".escodoo-feature-empty");
        this.groups = Array.from(this.el.querySelectorAll(".escodoo-feature-group"));
        this.rows = Array.from(this.el.querySelectorAll(".escodoo-feature-row"));
        return this._super(...arguments);
    },

    _onSearchInput(event) {
        if (!this.searchInput || event.target !== this.searchInput) {
            return;
        }
        const term = this.searchInput.value.trim().toLowerCase();
        let matches = 0;

        for (const row of this.rows) {
            const label = (row.dataset.escodooLabel || row.textContent).toLowerCase();
            const visible = !term || label.includes(term);
            row.hidden = !visible;
            if (visible) {
                matches += 1;
            }
        }

        // A category whose rows are all filtered out would otherwise leave its
        // heading and an empty table behind.
        for (const group of this.groups) {
            const hasVisibleRow = Array.from(
                group.querySelectorAll(".escodoo-feature-row")
            ).some((row) => !row.hidden);
            group.hidden = !hasVisibleRow;
        }

        if (this.emptyMessage) {
            this.emptyMessage.hidden = matches > 0;
        }
    },
});
