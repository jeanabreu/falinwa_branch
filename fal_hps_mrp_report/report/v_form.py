# -*- coding: utf-8 -*-
import time
from openerp.report import report_sxw
from openerp.osv import osv
from openerp import pooler

class v_form(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(v_form, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time ,
        })
        
report_sxw.report_sxw('report.v_form','mrp.production','fal_hps_mrp_report/report/v_form.rml',parser=v_form)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

