# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class account_invoice(orm.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'
    
    def _get_invoice_ids_fal(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('account.invoice.line').browse(cr, uid, ids, context=context):
            result[line.invoice_id.id] = True
        return result.keys()
    
    def _get_projects(self, cr, uid, ids, name, args, context=None):
        result = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            temp = []
            for line in invoice.invoice_line:
                if line.account_analytic_id and line.account_analytic_id.code not in temp:
                    temp.append(line.account_analytic_id.code or line.account_analytic_id.name)
            if temp:
                result[invoice.id] = "; ".join(temp)
            else:
                result[invoice.id] = ""
        return result
        
    _columns = {
        'fal_project_numbers' : fields.function(_get_projects, type='char',string='Projects',
            store={
                'account.invoice.line': (_get_invoice_ids_fal, [], 20),
            }, help="The projects."),
    }

#end of account_invoice()