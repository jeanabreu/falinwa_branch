from openerp.osv import fields, orm
from tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp import netsvc

class account_invoice(orm.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"
        
    _columns = {
        'purchase_ids': fields.many2many('purchase.order', 'purchase_invoice_rel', 'invoice_id', 'purchase_id', 'Purchases', readonly=True, help="Purchase Orders That related to Invoice"),
        'sale_ids': fields.many2many('sale.order', 'sale_order_invoice_rel', 'invoice_id', 'order_id', 'Sales', readonly=True, help="This is the list of sale that related to this Invoice"),
    }

#end of account_invoice()