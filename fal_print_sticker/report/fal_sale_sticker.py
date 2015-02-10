# -*- coding: utf-8 -*-
import time

from openerp import pooler
from openerp.osv import osv
from openerp.report import report_sxw
from openerp.tools.translate import _

class fal_sale_sticker(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(fal_sale_sticker, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_line_temp' : self._get_line_temp,
        })

    def _get_line_temp(self, sale_orders):
        temp = []
        for sale in sale_orders:
            for line in sale.order_line:
                if line.product_id.categ_id.isfal_finished_product:
                    for x in xrange(int(line.product_uom_qty)):
                        temp.append({
                            'fal_of_number' : 'this is of number',
                            'fal_sale_ref' : line.fal_sale_reference,
                        })
        return temp
        
report_sxw.report_sxw('report.fal.sale.sticker','sale.order','/fal_print_sticker/report/fal_sale_sticker.rml',parser=fal_sale_sticker)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
