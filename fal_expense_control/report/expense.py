# -*- coding: utf-8 -*-

import datetime
import time

from openerp.report import report_sxw

class expense(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(expense, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({'time': time, })

report_sxw.report_sxw('report.fal.hr.expense', 'hr.expense.expense', 'fal_expense_control/report/expense.rml',parser=expense)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

