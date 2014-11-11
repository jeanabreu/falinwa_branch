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

class purchase_order(orm.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"
    
    def _get_sale_order_invoiceterm(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if not ids:
            return res
        for order in self.browse(cr, uid, ids, context=context):
            val_order_policy = ''
            if order.sale_order_line_id.order_id is None:
                break
            elif order.sale_order_line_id.order_id.order_policy == 'manual' :
                val_order_policy = 'On Demand'
            elif order.sale_order_line_id.order_id.order_policy == 'picking' :
                val_order_policy = 'On Delivery Order'
            else:
                val_order_policy = 'Before Delivery'
            res[order.id] = val_order_policy
        return res
    
    _columns = {
        'sale_order_line_id': fields.many2one('sale.order.line','Sale Order Line'),
        'sale_order_line_order_id' : fields.related('sale_order_line_id','order_id',type="many2one",relation="sale.order",string="Sale Order",readonly=True),
        'sale_order_line_order_currency' : fields.related('sale_order_line_id','order_id','currency_id', type="many2one",relation="res.currency",string="Sale Order Currency",readonly=True),
        'sale_order_line_order_paymentterm' : fields.related('sale_order_line_id','order_id','payment_term', type="many2one",relation="account.payment.term",string="Sale Order Payment Term",readonly=True),
        'sale_order_line_order_invoiceterm' : fields.function(_get_sale_order_invoiceterm,type="char", string='Sale Order Invoice Term'),
        'fal_incoterm_id' : fields.many2one('stock.incoterms','Incoterm'),
    }

    def action_invoice_create(self, cr, uid, ids, context=None):
        order_id = self.pool.get('purchase.order').browse(cr, uid, ids, context)[0]
        res = super(purchase_order, self).action_invoice_create(cr, uid, ids, context)
        if not self.pool.get('account.invoice').browse(cr, uid, res).final_quotation_number:
            self.pool.get('account.invoice').write(cr, uid, res, {'final_quotation_number': order_id.quotation_number or order_id.name}, context)
        return res

    #overide the openerp real code
    def _create_pickings(self, cr, uid, order, order_lines, picking_id=False, context=None):
        """Creates pickings and appropriate stock moves for given order lines, then
        confirms the moves, makes them available, and confirms the picking.

        If ``picking_id`` is provided, the stock moves will be added to it, otherwise
        a standard outgoing picking will be created to wrap the stock moves, as returned
        by :meth:`~._prepare_order_picking`.

        Modules that wish to customize the procurements or partition the stock moves over
        multiple stock pickings may override this method and call ``super()`` with
        different subsets of ``order_lines`` and/or preset ``picking_id`` values.

        :param browse_record order: purchase order to which the order lines belong
        :param list(browse_record) order_lines: purchase order line records for which picking
                                                and moves should be created.
        :param int picking_id: optional ID of a stock picking to which the created stock moves
                               will be added. A new picking will be created if omitted.
        :return: list of IDs of pickings used/created for the given order lines (usually just one)
        """
        if not picking_id:
            picking_id = self.pool.get('stock.picking').create(cr, uid, self._prepare_order_picking(cr, uid, order, context=context))
        todo_moves = []
        stock_move = self.pool.get('stock.move')
        wf_service = netsvc.LocalService("workflow")
        for order_line in order_lines:
            if not order_line.product_id:
                continue
            if order_line.product_id.type in ('product', 'consu'):
                move = stock_move.create(cr, uid, self._prepare_order_line_move(cr, uid, order, order_line, picking_id, context=context))
                if order_line.move_dest_id:
                    #modify start here
                    if not order_line.move_dest_id.location_id:
                    #end here
                        order_line.move_dest_id.write({'location_id': order.location_id.id})
                todo_moves.append(move)
        stock_move.action_confirm(cr, uid, todo_moves)
        stock_move.force_assign(cr, uid, todo_moves)
        wf_service.trg_validate(uid, 'stock.picking', picking_id, 'button_confirm', cr)
        return [picking_id]
        
    def _prepare_order_picking(self, cr, uid, order, context=None):
        res = super(purchase_order, self)._prepare_order_picking(cr, uid, order, context)
        res['fal_project_number'] = order.order_line[0].account_analytic_id and order.order_line[0].account_analytic_id.code
        return res
        
#end of purchase_order()


class purchase_order_line(orm.Model):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"
    
    def onchange_qty(self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
            name=False, price_unit=False, context=None):
        """
        onchange handler of product_id.
        """
        if context is None:
            context = {}

        res = {'value': {'price_unit': price_unit or 0.0, 'name': name or '', 'product_uom' : uom_id or False}}
        if not product_id:
            return res

        product_product = self.pool.get('product.product')
        product_uom = self.pool.get('product.uom')
        res_partner = self.pool.get('res.partner')
        product_supplierinfo = self.pool.get('product.supplierinfo')
        product_pricelist = self.pool.get('product.pricelist')
        account_fiscal_position = self.pool.get('account.fiscal.position')
        account_tax = self.pool.get('account.tax')

        # - check for the presence of partner_id and pricelist_id
        #if not partner_id:
        #    raise osv.except_osv(_('No Partner!'), _('Select a partner in purchase order to choose a product.'))
        #if not pricelist_id:
        #    raise osv.except_osv(_('No Pricelist !'), _('Select a price list in the purchase order form before choosing a product.'))

        # - determine name and notes based on product in partner lang.
        context_partner = context.copy()
        if partner_id:
            lang = res_partner.browse(cr, uid, partner_id).lang
            context_partner.update( {'lang': lang, 'partner_id': partner_id} )
        product = product_product.browse(cr, uid, product_id, context=context_partner)

        # - set a domain on product_uom
        res['domain'] = {'product_uom': [('category_id','=',product.uom_id.category_id.id)]}

        # - check that uom and product uom belong to the same category
        product_uom_po_id = product.uom_po_id.id
        if not uom_id:
            uom_id = product_uom_po_id

        if product.uom_id.category_id.id != product_uom.browse(cr, uid, uom_id, context=context).category_id.id:
            if self._check_product_uom_group(cr, uid, context=context):
                res['warning'] = {'title': _('Warning!'), 'message': _('Selected Unit of Measure does not belong to the same category as the product Unit of Measure.')}
            uom_id = product_uom_po_id

        res['value'].update({'product_uom': uom_id})

        # - determine product_qty and date_planned based on seller info
        if not date_order:
            date_order = fields.date.context_today(self,cr,uid,context=context)


        supplierinfo = False
        for supplier in product.seller_ids:
            if partner_id and (supplier.name.id == partner_id):
                supplierinfo = supplier
                if supplierinfo.product_uom.id != uom_id:
                    res['warning'] = {'title': _('Warning!'), 'message': _('The selected supplier only sells this product by %s') % supplierinfo.product_uom.name }
                min_qty = product_uom._compute_qty(cr, uid, supplierinfo.product_uom.id, supplierinfo.min_qty, to_uom_id=uom_id)
                if (qty or 0.0) < min_qty: # If the supplier quantity is greater than entered from user, set minimal.
                    if qty:
                        res['warning'] = {'title': _('Warning!'), 'message': _('The selected supplier has a minimal quantity set to %s %s, you should not purchase less.') % (supplierinfo.min_qty, supplierinfo.product_uom.name)}
                    qty = min_qty
        dt = self._get_date_planned(cr, uid, supplierinfo, date_order, context=context).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        qty = qty or 1.0
        res['value'].update({'date_planned': date_planned or dt})
        if qty:
            res['value'].update({'product_qty': qty})

        return res
    
#end of purchase_order_line()
   

class procurement_order(orm.Model):
    _inherit = 'procurement.order'
    
    _columns = {
        'sale_order_line_id': fields.many2one('sale.order.line','Sale Order Line'),
    }
    
    #override real method from openerp code
    def make_po(self, cr, uid, ids, context=None):
        """ Make purchase order from procurement
        @return: New created Purchase Orders procurement wise
        """
        res = {}
        if context is None:
            context = {}
        company = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id
        partner_obj = self.pool.get('res.partner')
        uom_obj = self.pool.get('product.uom')
        pricelist_obj = self.pool.get('product.pricelist')
        prod_obj = self.pool.get('product.product')
        acc_pos_obj = self.pool.get('account.fiscal.position')
        seq_obj = self.pool.get('ir.sequence')
        warehouse_obj = self.pool.get('stock.warehouse')
        for procurement in self.browse(cr, uid, ids, context=context):
            res_id = procurement.move_id.id
            partner = procurement.product_id.seller_id # Taken Main Supplier of Product of Procurement.
            seller_qty = procurement.product_id.seller_qty
            partner_id = partner.id
            address_id = partner_obj.address_get(cr, uid, [partner_id], ['delivery'])['delivery']
            pricelist_id = partner.property_product_pricelist_purchase.id
            warehouse_id = warehouse_obj.search(cr, uid, [('company_id', '=', procurement.company_id.id or company.id)], context=context)
            uom_id = procurement.product_id.uom_po_id.id

            qty = uom_obj._compute_qty(cr, uid, procurement.product_uom.id, procurement.product_qty, uom_id)
            if seller_qty:
                qty = max(qty,seller_qty)

            price = pricelist_obj.price_get(cr, uid, [pricelist_id], procurement.product_id.id, qty, partner_id, {'uom': uom_id})[pricelist_id]

            schedule_date = self._get_purchase_schedule_date(cr, uid, procurement, company, context=context)
            purchase_date = self._get_purchase_order_date(cr, uid, procurement, company, schedule_date, context=context)

            #Passing partner_id to context for purchase order line integrity of Line name
            new_context = context.copy()
            new_context.update({'lang': partner.lang, 'partner_id': partner_id})

            product = prod_obj.browse(cr, uid, procurement.product_id.id, context=new_context)
            taxes_ids = procurement.product_id.supplier_taxes_id
            taxes = acc_pos_obj.map_tax(cr, uid, partner.property_account_position, taxes_ids)

            name = product.partner_ref
            if product.description_purchase:
                name += '\n'+ product.description_purchase
            #modif here
            if product.generic_product and procurement.sale_order_line_id.id:
                name = procurement.sale_order_line_id and procurement.sale_order_line_id.name
            #end here
            line_vals = {
                #make modification in here
                'name': name,
                'account_analytic_id' : procurement.sale_order_line_id and procurement.sale_order_line_id.order_id.project_id.id,
                'supplier_target_unit_price': procurement.sale_order_line_id and procurement.sale_order_line_id.supplier_target_unit_price,
                #end in here
                'product_qty': qty,
                'product_id': procurement.product_id.id,
                'product_uom': uom_id,
                'price_unit': price or 0.0,
                'date_planned': schedule_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                'move_dest_id': res_id,
                'taxes_id': [(6,0,taxes)],
            }
            name = seq_obj.get(cr, uid, 'purchase.order') or _('PO: %s') % procurement.name
            po_vals = {
                #make modification in here
                'sale_order_line_id':procurement.sale_order_line_id.id,
                'fal_incoterm_id' : procurement.sale_order_line_id and procurement.sale_order_line_id.order_id.incoterm.id,
                #end in here
                'name': name,
                'origin': procurement.origin,
                'partner_id': partner_id,
                'location_id': procurement.location_id.id,
                'warehouse_id': warehouse_id and warehouse_id[0] or False,
                'pricelist_id': pricelist_id,
                'date_order': purchase_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                'company_id': procurement.company_id.id,
                'fiscal_position': partner.property_account_position and partner.property_account_position.id or False,
                'payment_term_id': partner.property_supplier_payment_term.id or False,
            }
            res[procurement.id] = self.create_procurement_purchase_order(cr, uid, procurement, po_vals, line_vals, context=new_context)
            self.write(cr, uid, [procurement.id], {'state': 'running', 'purchase_id': res[procurement.id]})
        self.message_post(cr, uid, ids, body=_("Draft Purchase Order created"), context=context)
        return res
        
#end of procurement_order()