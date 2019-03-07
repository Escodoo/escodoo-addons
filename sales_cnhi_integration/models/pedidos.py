# -*- coding: utf-8 -*-

from odoo import models,fields,api
from odoo.exceptions import UserError
import base64

class SalePedidos(models.Model):
    _inherit = 'product.template'

    custom_product_id = fields.Integer(string='Id Prod', size=6)


class SaleImportPartner(models.Model):
    _inherit = 'res.partner'

    custom_cod_import = fields.Char(string='Codigo', size=14)



class Pedidos(models.Model):
    _name = 'sale.pedidos'
    file_input = fields.Binary('File input')

    ############################################
    # Header

    # ITP
    tipo_registro_itp = fields.Char(string='Tipo de Registro', size=3)
    ident_transacao = fields.Char(string='Identificação da Transação', size=3)
    versao_transacao = fields.Char(string='Versão da Transação')
    controle_movto = fields.Char(string='Controle da MOVTO')
    geracao_movto = fields.Char(string='Geração da MOVTO')
    hora_movto = fields.Char(string='Hora da MOVTO')
    gcg_transmissor = fields.Char(string='CGC Transmissor', size=14)
    #cgc_receptor = fields.Char(string='CGC Receptor', size=14)
    # cod_interreceptor = fields.Char(string='Referencia do Cliente', size=8

    # PA1
    tipo_registro_pa1 = fields.Char(string='Tipo de Registro', size=3)
    dt_programatu = fields.Char(string='Data Programada')
    # cond_pagamento = fields.Many2one('account.payment.term', string='Condição de Pagamento')
    ord_compra = fields.Char(string='Ordem de Compra', size=13)
    # desc_pedido = fields.Integer(string='Descrição do Pedido')
    desc_itm = fields.Char(string='Descrição do Item')
    tipo_pedido = fields.Char(size=1, string='Tipo do Pedido')
    item_iveco = fields.Char(string='Item IVECO', size=21)
    pedido_compra = fields.Char(string='Pedido de Compra', size=7)
    linha_pedido = fields.Integer(string='Linha do Pedido')
    cod_clie = fields.Char(string='Referência do Pedido', size=8)

    ############################################
    # Itens

    # PA2
    codigo_pedido = fields.Char(string= 'Codigo', size=6)
    dt_entrega = fields.Char(string='Data de Entrega', size=6)
    status_entrega = fields.Char(string='Status da Entrega', size=2)
    qtde_chamadas = fields.Integer(string='Quantidade', size=9)
    valor_unitario = fields.Integer(string='Valor Unitario', size=15)


    ############################################
    # Others

    lista_item = fields.Char(string='Mais um')

    #cliente = fields.Char(string='Cliente')
    faturamento = fields.Integer(string='Faturamento')

    state = fields.Selection([('draft', 'Rascunho'),
                              ('load', 'Carregado'),
                              ('valid', 'Validada'),
                              ])
    sale_id = fields.Many2one('sale.order')

    item_pa1 = {}
    item_pa2 = {}

    @api.multi
    def import_pedido(self):
        if not self.file_input:
            raise UserError('Por favor, insira um arquivo de Pedido.')
        lista = base64.b64decode(self.file_input)

        self.tipo_registro_itp = (lista[:3])
        self.ident_transacao = (lista[3:6])
        self.versao_transacao = (lista[6:8])
        self.controle_movto = (lista[8:13])
        self.geracao_movto = (lista[13:19])
        # self.geracao_movto = self.date_formated
        self.hora_movto = (lista[19:25])
        self.gcg_transmissor = (lista[25:39])
        self.cgc_receptor = (lista[39:54])

        y = (len(lista)/129)
        x = ((y - 2)/2)
        u = 129
        
        self.desc_itm = 18

        for i in range(int(x)):
            self.item_pa1[i] = lista[int(u):(int(u)+129)]            
            self.item_pa2[i] = lista[int(u+129):(int(u)+258)]

        # PA1
        #self.tipo_registro_pa1 = lista[130:133]
        #self.dt_programatu = lista[145:152]
        #self.ord_compra = lista[166:176]
        #self.desc_itm = lista[200:204]
        #self.tipo_pedido = lista[204:205]
        #self.item_iveco = lista[205:214]
        #self.pedido_compra = lista[226:233]
        #self.linha_pedido = lista[237:243]
        #self.cod_clie = lista[243:250]

        #PA2
        #self.tipo_registro_pa2 = lista[260:263]
        #self.dt_entrega = lista[263:269]
        #self.status_entrega = lista[269:271]
#        self.qtde_chamadas = (lista[269:278])
#        self.valor_unitario = (lista[278:293])


        self.lista_pedido = lista[390:392]


        self.state = "load"


    def gerar_fatura(self):

        client = self.env['res.partner'].search(
             [('custom_cod_import', '=', self.gcg_transmissor)], limit=1)

        if not client:
            client = self.env['res.partner'].create({
                'custom_cod_import': self.gcg_transmissor,
                'name': "Cadastro via sistema "+ self.gcg_transmissor,

                'invoice_warn': "no-message",
                'picking_warn': "no-message",
                'purchase_warn': "no-message",
                'sale_warn': "no-message",
                #'property_account_receivable_id': 1,
                #'property_account_payable_id': 1,
            })


        sale = self.env['sale.order'].create({
            'partner_id': client.id,
            'currency_id': 1,
            'date_order': "2019-03-05",
            'picking_policy': "direct",
            'pricelist_id': client.property_product_pricelist.id,
        })

        for i in range(len(self.item_pa1)):
            product = self.env['product.template'].search(
                [('custom_product_id', '=', self.desc_itm)], limit=1)

            if not product:
                product = self.env['product.template'].create({
                    'custom_product_id' : self.desc_itm,
                    'type' : 'product',
                    'name' : 'Desenvolvimento',
                    'uom_id' : 1,
                    'uom_po_id' : 1,
                    'responsible_id' : 1,
                    'tracking' : 'none',
                    'categ_id' : 4,
                    'sale_line_warm' : 'no-message',
                    'fiscal_type' : 'product',
                    })

 
            sale_line = self.env['sale.order.line'].create({
                            'custom_product_id' : self.desc_itm,
                            'order_id': sale.id,
                            'product_id': product.id,
                            'product_uom': 1,
                            'price_unit': 100,
                            'product_uom_qty': 5
                        })


        self.sale_id = sale.id
        self.state = "valid"




