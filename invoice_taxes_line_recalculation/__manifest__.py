# -*- coding: utf-8 -*-
# © 2018 Johny Chen Jy <johnychenjy@gmail.com>, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{   # pylint: disable=C8101,C8103
    'name': 'Invoice Line Taxes Recalculation',
    'summary': """Invoice Line Taxes Recalculation""",
    'version': '11.0.1.0.0',
    'category': 'NFE',
    'author': 'Trustcode, Escodoo',
    'license': 'AGPL-3',
    'website': 'http://www.Trustcode.com.br',
    'contributors': [
        'Johny Chen Jy <johnychenjy@gmail.com>',
        'Marcel Savegnago <marcel.savegnago@gmail.com>',
    ],
    'depends': [
        'br_account',
    ],
    'data': [
        'views/account_invoice_views.xml'
    ],
}
