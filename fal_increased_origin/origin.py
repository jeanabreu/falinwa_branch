# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class sale_order(orm.Model):
    _name = "sale.order"
    _inherit = "sale.order"
    
    _columns = {
        'origin': fields.char('Source Document', size=512, help="Reference of the document that generated this sales order request."),
    }
#end of sale_order()

class purchase_order(orm.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"
    
    _columns = {
        'origin': fields.char('Source Document', size=512,
            help="Reference of the document that generated this purchase order request; a sales order or an internal procurement request."
        ),
    }
#end of purchase_order()

class account_invoice(orm.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"
    _columns = {
        'origin': fields.char('Source Document', size=512, help="Reference of the document that produced this invoice.", readonly=True, states={'draft':[('readonly',False)]}),
    }
#end of account_invoice()

class account_voucher(orm.Model):
    _name = "account.voucher"
    _inherit = "account.voucher"
    
    _columns = {
        'name':fields.char('Memo', size=512, readonly=True, states={'draft':[('readonly',False)]}),
    }

#end of account_voucher()

class procurement_order(orm.Model):
    _name = "procurement.order"
    _inherit = 'procurement.order'
    _columns = {
        'origin': fields.char('Source Document', size=512,
            help="Reference of the document that created this Procurement.\n"
            "This is automatically completed by OpenERP."),
    }

#end of procurement_order()

class mrp_production(orm.Model):
    _name = 'mrp.production'
    _inherit = 'mrp.production'
    _columns = {
        'origin': fields.char('Source Document', size=512, readonly=True, states={'draft': [('readonly', False)]},
            help="Reference of the document that generated this production order request."),
    }
#end of mrp_production()

class mrp_bom(orm.Model):
    _name = 'mrp.bom'
    _inherit = 'mrp.bom'
    _columns = {
        'name': fields.char('Name', size=512),
        'code': fields.char('Reference', size=512),
    }
#end of mrp_bom()

class stock_picking(orm.Model):
    _name = "stock.picking"
    _inherit = 'stock.picking'
    
    _columns = {
        'origin': fields.char('Source Document', size=512, states={'done':[('readonly', True)], 'cancel':[('readonly',True)]}, help="Reference of the document", select=True),
    }
#end of stock_picking()

class stock_move(orm.Model):
    _name = "stock.move"
    _inherit = "stock.move"
    
    _columns = {
        'origin': fields.related('picking_id','origin',type='char', size=512, relation="stock.picking", string="Source", store=True),
    }
#end of stock_move()