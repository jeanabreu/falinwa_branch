# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import netsvc
from openerp import pooler
from openerp.osv import orm, fields
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp import tools

class procurement_order(orm.Model):
    _inherit = 'procurement.order'
    
    def _procure_orderpoint_confirm(self, cr, uid, automatic=False,\
            use_new_cursor=False, context=None, user_id=False):
        '''
        Create procurement based on Orderpoint
        use_new_cursor: False or the dbname

        @param self: The object pointer
        @param cr: The current row, from the database cursor,
        @param user_id: The current user ID for security checks
        @param context: A standard dictionary for contextual values
        @param param: False or the dbname
        @return:  Dictionary of values
        """
        '''
        if context is None:
            context = {}
        if use_new_cursor:
            cr = pooler.get_db(use_new_cursor).cursor()
        orderpoint_obj = self.pool.get('stock.warehouse.orderpoint')
        
        procurement_obj = self.pool.get('procurement.order')
        wf_service = netsvc.LocalService("workflow")
        offset = 0
        ids = [1]
        if automatic:
            self.create_automatic_op(cr, uid, context=context)
        while ids:
            ids = orderpoint_obj.search(cr, uid, [], offset=offset, limit=100)
            for op in orderpoint_obj.browse(cr, uid, ids, context=context):
                prods = self._product_virtual_get(cr, uid, op)
                if prods is None:
                    continue
                if prods < op.product_min_qty:
                    #Hans Falinwa modify begin here (use logic field to diffrent method. Use product_order_label_qty if logic fields is fix)
                    if op.logic == 'fix':
                        qty = op.product_order_label_qty
                    else:
                        qty = max(op.product_min_qty, op.product_max_qty)-prods

                    reste = qty % op.qty_multiple
                    if reste > 0:
                        qty += op.qty_multiple - reste

                    if qty <= 0:
                        continue
                    if op.product_id.type not in ('consu'):
                        if op.procurement_draft_ids:
                        # Check draft procurement related to this order point
                            pro_ids = [x.id for x in op.procurement_draft_ids]
                            procure_datas = procurement_obj.read(
                                cr, uid, pro_ids, ['id', 'product_qty'], context=context)
                            to_generate = qty
                            for proc_data in procure_datas:
                                if to_generate >= proc_data['product_qty']:
                                    wf_service.trg_validate(uid, 'procurement.order', proc_data['id'], 'button_confirm', cr)
                                    procurement_obj.write(cr, uid, [proc_data['id']],  {'origin': op.name}, context=context)
                                    to_generate -= proc_data['product_qty']
                                if not to_generate:
                                    break
                            qty = to_generate

                    if qty:
                        proc_id = procurement_obj.create(cr, uid,
                                                         self._prepare_orderpoint_procurement(cr, uid, op, qty, context=context),
                                                         context=context)
                        wf_service.trg_validate(uid, 'procurement.order', proc_id,
                                'button_confirm', cr)
                        wf_service.trg_validate(uid, 'procurement.order', proc_id,
                                'button_check', cr)
                        orderpoint_obj.write(cr, uid, [op.id],
                                {'procurement_id': proc_id}, context=context)
            offset += len(ids)
            if use_new_cursor:
                cr.commit()
        if use_new_cursor:
            cr.commit()
            cr.close()
        return {}

#end of procurement_order()