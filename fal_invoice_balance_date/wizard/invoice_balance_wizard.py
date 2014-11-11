# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _

class invoice_balance_wizard(orm.TransientModel):
    _name = "invoice.balance.wizard"
    _description = "Invoice Balance Wizard"
    
    _columns = {
        'to_date': fields.date('To' , required=True),
        'type': fields.selection([
            ('all','All'),
            ('out_invoice','Customer Invoice'),
            ('in_invoice','Supplier Invoice'),
            ('out_refund','Customer Refund'),
            ('in_refund','Supplier Refund'),
            ],'Type', select=True, change_default=True, required=True),
    }
    
    def search_invoice_balance_date(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data_wizard = self.read(cr, uid, ids, [])[0]
        domain = []
        if data_wizard['type'] != 'all':
            domain = [('type','=',data_wizard['type']),('state','not in', ['draft','cancel']),('date_invoice','<=',data_wizard['to_date']),('amount_balance_date','!=',0.00)]
        context['wizard_data_date'] = data_wizard['to_date']
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices Balance Based on '+ str(data_wizard['to_date']),
            'res_model': 'account.invoice',
            'view_mode': 'tree',
            'view_type': 'form',
            'view_id': self.pool.get('ir.model.data').get_object_reference(cr, uid, 'fal_invoice_balance_date', 'invoice_tree_fal_balance_date')[1],
            'domain' : domain,
            'target': 'current',
            'context' : context,
            }
        
#end of invoice_balance_wizard()