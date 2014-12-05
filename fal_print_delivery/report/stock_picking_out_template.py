# -*- coding: utf-8 -*-
import time

from openerp import pooler
from openerp.report import report_sxw
from openerp.tools.translate import _

class stock_picking_out_template(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(stock_picking_out_template, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
        })
        
report_sxw.report_sxw('report.fwa.stock.picking.out.template','stock.picking.out','/fal_print_delivery/report/stock_picking_out_template.rml',parser=stock_picking_out_template)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
