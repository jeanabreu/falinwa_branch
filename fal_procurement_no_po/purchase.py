# -*- coding: utf-8 -*-
import time
import pytz
from openerp import SUPERUSER_ID
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp.osv import fields, orm
from openerp import netsvc
from openerp import pooler
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.osv.orm import browse_record, browse_null
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP

class product_template(orm.Model):
    
    _name = "product.template"
    _inherit = "product.template"

    _columns = {
        'fal_proc_po_disable' : fields.boolean('Procurement PO Disable'),
    }
    
    _defaults = {
        'fal_proc_po_disable' : True,
    }
    
#end of product_product()

class procurement_order(orm.Model):
    
    _name = "procurement.order"
    _inherit = 'procurement.order'
    
    def check_buy(self, cr, uid, ids, context=None):
        ''' return True if the supply method of the mto product is 'buy'
        '''
        for procurement in self.browse(cr, uid, ids, context=context):
            if procurement.product_id.fal_proc_po_disable:
                return False
        return super(procurement_order,self).check_buy(cr, uid, ids, context)
    
    def _check_make_to_stock_product(self, cr, uid, procurement, context=None):
        """ Checks procurement move state.
        @param procurement: Current procurement.
        @return: True or move id.
        """
        ok = True
        if procurement.move_id:
            message = False
            id = procurement.move_id.id
            if not (procurement.move_id.state in ('done','assigned','cancel')):
                ok = ok and self.pool.get('stock.move').action_assign(cr, uid, [id])
                if procurement.product_id.fal_proc_po_disable and procurement.product_id.supply_method == 'buy':
                    message = _("This procurement is lock because we disable the procurement.")
                    if message and not ok:
                        message = _("Procurement '%s' is in exception: ") % (procurement.name) + message
                        #temporary context passed in write to prevent an infinite loop
                        ctx_wkf = dict(context or {})
                        ctx_wkf['workflow.trg_write.%s' % self._name] = False
                        self.write(cr, uid, [procurement.id], {'message': message},context=ctx_wkf)
                    return ok
        return super(procurement_order,self)._check_make_to_stock_product(cr, uid, procurement, context)
        
#end of procurement_order()