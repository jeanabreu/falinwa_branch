# -*- coding: utf-8 -*-
import time

from openerp import pooler
from openerp.osv import osv
from openerp.report import report_sxw
from openerp.tools.translate import _

class product_label(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(product_label, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'getMaxQty': self._get_max_qty,
            'getMinQty': self._get_min_qty,
            'getOrderQty': self._get_order_qty,
        })

    def _get_order_qty(self, order_point_ids):
        for order_point_id in order_point_ids:
            order_qty = order_point_id.product_order_label_qty
        return float(order_qty)
        
    def _get_max_qty(self, order_point_ids):
        for order_point_id in order_point_ids:
            max_qty = order_point_id.product_max_qty
        return float(max_qty)
        
    def _get_min_qty(self, order_point_ids):
        for order_point_id in order_point_ids:
            min_qty = order_point_id.product_min_qty
        return float(min_qty)
        
report_sxw.report_sxw('report.fwa.product.product.label','product.product','/product_label_report/report/product_label.rml',parser=product_label)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
