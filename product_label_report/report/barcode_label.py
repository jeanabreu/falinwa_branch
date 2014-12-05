# -*- coding: utf-8 -*-
import time

from openerp import pooler
from openerp.osv import osv
from openerp.report import report_sxw
from openerp.tools.translate import _

class barcode_label(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(barcode_label, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
        })
        
report_sxw.report_sxw('report.fwa.product.barcode','product.product','/product_label_report/report/barcode_label.rml',parser=barcode_label)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
