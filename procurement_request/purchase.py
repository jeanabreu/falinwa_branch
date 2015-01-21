# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import netsvc

class purchase_order(orm.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"
    
    STATE_SELECTION = [
        ('procurement_request', 'Procurement Request'),
        ('draft', 'Draft PO'),
        ('sent', 'RFQ Sent'),
        ('validated', 'Validated'),
        ('confirmed', 'Waiting Approval'),
        ('approved', 'Purchase Order'),
        ('except_picking', 'Shipping Exception'),
        ('except_invoice', 'Invoice Exception'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ]
    _columns = {
        'state': fields.selection(STATE_SELECTION, 'Status', readonly=True, help="The status of the purchase order or the quotation request. A quotation is a purchase order in a 'Draft' status. Then the order has to be confirmed by the user, the status switch to 'Confirmed'. Then the supplier must confirm the order to change the status to 'Approved'. When the purchase order is paid and received, the status becomes 'Done'. If a cancel action occurs in the invoice or in the reception of goods, the status becomes in exception.", select=True, track_visibility='onchange'),
        'req_product_id' : fields.many2one('product.product', 'Product', domain=[('purchase_ok','=',True)], change_default=True),
        'req_product_description' : fields.text('Description'),
        'req_product_qty' : fields.float('Quantity', digits_compute=dp.get_precision('Product Unit of Measure')),
        'req_uom_id' : fields.many2one('product.uom', string="UOM"),
        'warehouse_manager_comment' : fields.text('Warehouse Manager Comment'),
    }
    
    def onchange_req_product_id(self, cr, uid, ids, req_product_id, context=None):
        if not req_product_id:
            return {}        
        product_id = self.pool.get('product.product').browse(cr, uid, req_product_id, context=context)
        return {'value': {'req_product_description': product_id.name,'req_uom_id': product_id.uom_po_id.id}}
    
    
    def _get_supplier(self, cr, uid, context=None):
        if context is None:
            context = {}
        supplier_obj = self.pool.get('res.partner')
        res = supplier_obj.search(cr, uid, [('name', '=', 'SUPPLIER TO BE DEFINED'),
                                            ('supplier', '=', True)],
                                                limit=1)
        return res and res[0] or False  
        
    _defaults = {
        'state': 'procurement_request',
        'partner_id': _get_supplier,
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('req_product_id', False):
            uom_obj = self.pool.get('product.uom')
            pricelist_obj = self.pool.get('product.pricelist')
            acc_pos_obj = self.pool.get('account.fiscal.position')
            product_obj = self.pool.get('product.product')
            partner_obj = self.pool.get('res.partner')
            order_line_obj = self.pool.get('purchase.order.line')
            product_uom = self.pool.get('product.uom')
            
            company = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id        
            product_id = product_obj.browse(cr, uid, vals['req_product_id'])
            partner_id = partner_obj.browse(cr, uid, vals['partner_id'])
 
            qty = uom_obj._compute_qty(cr, uid, vals.get('req_uom_id', False) or product_id.uom_po_id.id, vals.get('req_product_qty',0), vals.get('req_uom_id', False) or product_id.uom_po_id.id)
            price = pricelist_obj.price_get(cr, uid, [partner_id.property_product_pricelist_purchase.id], product_id.id, qty, partner_id.id, {'uom': vals.get('req_uom_id', False) or product_id.uom_po_id.id})[partner_id.property_product_pricelist_purchase.id]
            taxes_ids = product_id.supplier_taxes_id
            taxes = acc_pos_obj.map_tax(cr, uid, partner_id.property_account_position, taxes_ids)
            
            supplierinfo = False
            for supplier in product_id.seller_ids:
                if partner_id and (supplier.name.id == partner_id.id):
                    supplierinfo = supplier
                    #if supplierinfo.product_uom.id != uom_id:
                    #    res['warning'] = {'title': _('Warning!'), 'message': _('The selected supplier only sells this product by %s') % supplierinfo.product_uom.name }
                    #min_qty = product_uom._compute_qty(cr, uid, supplierinfo.product_uom.id, supplierinfo.min_qty, to_uom_id=uom_id)
                    #if (qty or 0.0) < min_qty: # If the supplier quantity is greater than entered from user, set minimal.
                    #    if qty:
                    #        res['warning'] = {'title': _('Warning!'), 'message': _('The selected supplier has a minimal quantity set to %s %s, you should not purchase less.') % (supplierinfo.min_qty, supplierinfo.product_uom.name)}
                    #    qty = min_qty
            if supplierinfo:
                dt = order_line_obj._get_date_planned(cr, uid, supplierinfo, vals['date_order'], context=context).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            else:
                dt = datetime.strptime(vals['date_order'], DEFAULT_SERVER_DATE_FORMAT) + relativedelta(days=product_id.produce_delay)
            vals['order_line'] = [(0,0,{
                'product_id' : product_id.id,
                'name' : vals.get('req_product_description', False) or product_id.name,
                'product_qty' : qty or 0,
                'product_uom' : vals.get('req_uom_id', False) or product_id.uom_po_id.id,
                'price_unit' :  price,
                'date_planned': vals.get('minimum_planned_date', False) or dt,
                'taxes_id': [(6,0,taxes)],
                'warehouse_manager_comment' : vals.get('warehouse_manager_comment', False)
            })]
        else :
            if vals.get('order_line', False):
                vals['req_product_id'] = vals['order_line'][0][2].get('product_id')
                vals['req_product_description'] = vals['order_line'][0][2].get('name',False)
                vals['req_product_qty'] = vals['order_line'][0][2].get('product_qty',0)
                vals['warehouse_manager_comment'] = vals['order_line'][0][2].get('warehouse_manager_comment',0)
                vals['req_uom_id'] = vals['order_line'][0][2].get('product_uom',False)
      
        return super(purchase_order, self).create(cr, uid, vals, context=context)
    
    def write(self, cr, uid, ids, vals, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        order_line_obj = self.pool.get('purchase.order.line')
        val = {'name' :'', 'product_qty' : '','warehouse_manager_comment': '','product_uom': ''}
        for purchase_id in self.browse(cr, uid, ids, context):
            if purchase_id.order_line:
                val = {
                    'name' : purchase_id.order_line[0].name,
                    'product_qty' : purchase_id.order_line[0].product_qty,
                    'warehouse_manager_comment' : purchase_id.order_line[0].warehouse_manager_comment,
                    'product_uom' : purchase_id.order_line[0].product_uom.id,
                }
                if vals.get('req_product_id',False):
                    val.update({'product_id' : vals.get('req_product_id',False)})
                if vals.get('req_product_description',False):
                    val.update({'name' : vals.get('req_product_description',False)})
                if vals.get('req_product_qty', 0):
                    val.update({'product_qty': vals.get('req_product_qty', 0)})
                if vals.get('warehouse_manager_comment', False):
                    val.update({'warehouse_manager_comment': vals.get('warehouse_manager_comment', False)})
                if vals.get('req_uom_id', False):
                    val.update({'product_uom': vals.get('req_uom_id', False)})
                order_line_obj.write(cr, uid, purchase_id.order_line[0].id, val, context=context)
        return super(purchase_order, self).write(cr, uid, ids, vals, context=context)

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default.update({
            'req_product_id' : False,
            'req_product_description' : '',
            'req_product_qty' : 0.00,
            'req_uom_id' : False,
            'warehouse_manager_comment' : ''
        })
        return super(purchase_order, self).copy(cr, uid, id, default, context)
        
    def unlink(self, cr, uid, ids, context=None):
        purchase_orders = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for s in purchase_orders:
            if s['state'] in ['draft','cancel','procurement_request']:
                unlink_ids.append(s['id'])
            else:
                raise orm.except_orm(_('Invalid Action!'), _('In order to delete a purchase order, you must cancel it first.'))

        # automatically sending subflow.delete upon deletion
        wf_service = netsvc.LocalService("workflow")
        for id in unlink_ids:
            wf_service.trg_validate(uid, 'purchase.order', id, 'purchase_cancel', cr)

        return super(purchase_order, self).unlink(cr, uid, unlink_ids, context=context)
        
    def action_mark_rfq(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'draft'})

    #TODO: implement messages system
    def wkf_confirm_order(self, cr, uid, ids, context=None):
        todo = []
        for po in self.browse(cr, uid, ids, context=context):
            if not po.order_line:
                raise orm.except_orm(_('Error!'),_('You cannot confirm a purchase order without any purchase order line.'))
            if po.partner_id.name == 'SUPPLIER TO BE DEFINED':
                raise orm.except_orm(_('Invalid Action!'), _('In order to confirm a quotation, you must define supplier first.'))
        return super(purchase_order, self).wkf_confirm_order(cr, uid, ids, context)

    def _prepare_order_line_move(self, cr, uid, order, order_line, picking_id, group_id, context=None):
        res = super(purchase_order, self)._prepare_order_line_move(cr, uid, order, order_line, picking_id, group_id, context=context)
        for rex in res:
            res['fal_warehouse_manager_comment'] = order_line.warehouse_manager_comment
        return res
    
#end of purchase_order()

class purchase_order_line(orm.Model):
    _name = 'purchase.order.line'
    _inherit = 'purchase.order.line'
    
    _columns = {
        'warehouse_manager_comment' : fields.text('Warehouse Manager Comment'),
    }

#end of purchase_order_line()