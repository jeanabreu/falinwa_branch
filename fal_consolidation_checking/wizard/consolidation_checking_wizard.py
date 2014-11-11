# -*- coding: utf-8 -*-
from openerp.osv import orm, fields
from openerp.tools.translate import _
from openerp import netsvc
from openerp import SUPERUSER_ID

class consolidation_checking_wizard(orm.TransientModel):
    _name = "fal.consolidation.checking.wizard"
    _description = "Falinwa Consolidation Checking Wizard"
    
    _columns = {
        'partner_id' : fields.many2one('res.partner','Partner', required=True),
        'fal_consolidation_checking_line' : fields.one2many('fal.consolidation.checking.wizard.line', 'consolidation_checking_id', 'Children Assets', readonly=True),
    }

    def onchange_partner(self, cr, uid, ids, partner_id, context=None):
        res = {}
        invoice_obj = self.pool.get('account.invoice')
        user_obj = self.pool.get('res.users')        
        res['fal_consolidation_checking_line'] = []
        temp = []
        user_id = user_obj.browse(cr, uid, uid)
        if partner_id :
            args = [('type','=','out_invoice'), ('state','=','paid'), ('company_id','=',user_id.company_id.id), ('partner_id','=',partner_id)]
            for customer_ivoice_id in invoice_obj.browse(cr, uid, invoice_obj.search(cr, uid, args)):
                supplier_invoice_id = invoice_obj.search(cr, SUPERUSER_ID, [('number','=',customer_ivoice_id.name), ('type','=','in_invoice'), ('state','=','paid')]) or False
                other_supplier_invoice_number = ''
                other_supplier__invoice_total = 0.00
                other_supplier__invoice_currency = ''
                if supplier_invoice_id:
                    supplier_invoice_id = invoice_obj.browse(cr, SUPERUSER_ID, supplier_invoice_id[0], context=context)
                    other_supplier_invoice_number = "%s ;%s" % (supplier_invoice_id.number, supplier_invoice_id.name or '')
                    other_supplier__invoice_total = supplier_invoice_id.amount_total
                    other_supplier__invoice_currency = supplier_invoice_id.currency_id.symbol
                temp.append((0, 0, {
                    'current_customer_invoice_number' : "%s ;%s" % (customer_ivoice_id.number ,customer_ivoice_id.name or ''),
                    'other_supplier_invoice_number' : other_supplier_invoice_number,
                    'current_customer_invoice_total' : customer_ivoice_id.amount_total,
                    'other_supplier__invoice_total' : other_supplier__invoice_total,
                    'current_customer_invoice_currency' : customer_ivoice_id.currency_id.symbol,
                    'other_supplier__invoice_currency' : other_supplier__invoice_currency,
                }))
            res['fal_consolidation_checking_line'] = temp
        return {'value' : res}
    
#end of consolidation_checking_wizard()

class consolidation_checking_wizard_line(orm.TransientModel):
    _name = "fal.consolidation.checking.wizard.line"
    _description = "Falinwa Consolidation Checking Wizard Line"
    
    _columns = {
        'consolidation_checking_id' : fields.many2one('fal.consolidation.checking.wizard', 'Consolidated Checking Wizard'),
        'current_customer_invoice_number' : fields.char('Current Company Customer Invoice Number', size=128), 
        'other_supplier_invoice_number' : fields.char('Other Company Supplier Invoice Number', size=128),
        'current_customer_invoice_total' : fields.float('Current Company Customer Invoice Total'), 
        'other_supplier__invoice_total' : fields.float('Other Company Supplier Invoice Total'),
        'current_customer_invoice_currency' : fields.char('Current Company Customer Invoice Currency', size=64), 
        'other_supplier__invoice_currency' : fields.char('Other Company Supplier Invoice Currency', size=64),
    }

#end of consolidation_checking_wizard_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
