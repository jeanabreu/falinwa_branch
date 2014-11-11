# -*- coding: utf-8 -*-
import time
from openerp.report import report_sxw
from openerp.osv import osv
from openerp import pooler

class fapiao(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(fapiao, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'user': self.pool.get('res.users').browse(cr, uid, uid, context),
        })
        
        
report_sxw.report_sxw('report.fapiao','fapiao','l10n_cn_fapiao/report/fapiao.rml',parser=fapiao)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

