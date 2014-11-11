# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from collections import defaultdict

from openerp import pooler
from openerp.report import report_sxw

class account_payment_print(report_sxw.rml_parse):
    _name = "account_payment_print"

    def __init__(self, cr, uid, name, context=None):
        super(account_payment_print, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time
        })

report_sxw.report_sxw('report.payment_print',
        'account.voucher', 'fal_payment_document/report/account_payment_print.rml',
        parser=account_payment_print)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
