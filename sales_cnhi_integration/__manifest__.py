# -*- coding: utf-8 -*-
# Copyright 2016, 2017 Openworx
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "ECOD3 - Remessa de Pedidos",
    "summary": "Remessa (Nome, descricao e sinapse)",
    "version": "11.0.1.0.2",
    "category": "vendas",
    "website": "https://ecod3.com",
    "description": """
		Exemplos de campos do Odoo.
    """,
    'images':[
	],
    "author": "ECOD3",
    "license": "LGPL-3",
    "installable": True,
    "depends": [ 'base', 'contacts', 'sale' ],

    "data": [
        'views/pedidos.xml',
        'views/sale_import_partner.xml',
        'views/product.xml',
        #'views/file.xml',
        
    ],
}

