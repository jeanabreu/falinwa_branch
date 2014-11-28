# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _

class fapiao(orm.Model):
    _name = "fapiao"
    _inherit = ['mail.thread']
    _order = "fapiao_date desc, id desc"
    _description = "Fapiao"
    
    def _get_fapiao_line(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('fapiao.line').browse(cr, uid, ids, context=context):
            result[line.fapiao_id.id] = True
        return result.keys()
        
    def _amount_total_fapiao(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for fapiao in self.browse(cr,uid,ids,context=context):
            total_fapiao_amount = 0
            for fapiao_line in fapiao.fapiao_line_ids :
                if not fapiao_line.not_fapiao:
                    total_fapiao_amount += fapiao_line.allocated_ammount
            res[fapiao.id] = total_fapiao_amount
        return res

    def _total_amount_tax_fapiao(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for fapiao in self.browse(cr, uid, ids, context=context):
            total_fapiao_amount = 0.00
            total_tax_fapiao_amount = 0.00
            tax_obj = self.pool.get('account.tax')
            for fapiao_line in fapiao.fapiao_line_ids :
                if not fapiao_line.not_fapiao:                    
                    total_fapiao_amount += fapiao_line.allocated_ammount
            if fapiao.tax_id:
                total_tax_fapiao_amount = total_fapiao_amount / (1 + fapiao.tax_id.amount) * fapiao.tax_id.amount
            res[fapiao.id] = total_tax_fapiao_amount
        return res
        
    _columns = {
        'name' : fields.char("Fapiao Sequence Number",size=64),
        'fapiao_type': fields.selection(
            [('customer', 'Customer'), ('supplier', 'Supplier'),
             ('customer_credit_note', 'Customer Credit note'),
             ('customer_credit_note', 'Customer Credit note')],
            'Fapiao Type', required=True),
        'tax_id': fields.many2one('account.tax', 'Tax'),
        'total_tax_amount': fields.function(_total_amount_tax_fapiao, digits_compute=dp.get_precision('Account'), string='Total Tax Amount',
            store={
                'fapiao': (lambda self, cr, uid, ids, c={}: ids, ['fapiao_line_ids','tax_type','state'], 20),
                'fapiao.line': (_get_fapiao_line, ['allocated_ammount'], 20),
            }, help="The tax amount of Fapiao."),
        'partner_id': fields.many2one('res.partner', 'Partner', required=True),
        'fapiao_number': fields.char("Fapiao Number", size=64, required=True),
        'fapiao_date': fields.date(string="Fapiao Date", required=True),
        'fapiao_declaration_date': fields.date(string="Declaration Date"),
        'reception_date': fields.date(string="Reception Date"),
        'amount_with_taxes': fields.function(_amount_total_fapiao, digits_compute=dp.get_precision('Account'), string='Total Fapiao Amount',
            store={
                'fapiao': (lambda self, cr, uid, ids, c={}: ids, ['fapiao_line_ids','state'], 20),
                'fapiao.line': (_get_fapiao_line, ['allocated_ammount'], 20),
            }, help="The total amount of Fapiao."),
        'fapiao_line_ids' : fields.one2many('fapiao.line','fapiao_id','Fapiao Line'),
        'tag_ids': fields.many2many('fapiao.tag.line', string="Tags"),
        'notes': fields.text(string="Notes"),
        'state': fields.selection([('Draft', 'Draft'), ('Posted', 'Posted')], 'Status', readonly=True, required=True),
        'company_id': fields.many2one('res.company', 'Company', required=True, readonly=True),
    }

    _defaults = {
        'state': 'Draft',
        'fapiao_date' : fields.date.context_today,
        'company_id': lambda self,cr,uid,c: self.pool.get('res.users').browse(cr, uid, uid, c).company_id.id,
    }
    
    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        if context is None:
            context = {}
        res = {}
        invoice_obj = self.pool.get('account.invoice')
        partner_obj = self.pool.get('res.partner')
        fapiao_line_obj = self.pool.get('fapiao.line')
        
        #part need to be fixed
        typeinvoice = False
        if context.get('default_fapiao_type',False) == 'customer':
            typeinvoice = 'out_invoice'
        if context.get('default_fapiao_type',False) == 'supplier':
            typeinvoice = 'in_invoice'
        invoice_ids = invoice_obj.search(cr, uid, [('commercial_partner_id','=',partner_id),('state','!=','cancel'),('type','=',typeinvoice)], context=context)
        temp = []
        for fapiao in self.browse(cr, uid, ids , context=context):
            temp_line = []
            for fapiao_line_id in fapiao.fapiao_line_ids:
                temp_line.append((2,fapiao_line_id.id))
            if temp_line:
                temp += temp_line
        for invoice_id in invoice_obj.browse(cr, uid, invoice_ids, context=context) :
            allocated_amount_posted = 0.00
            fapiao_line_posted_ids = fapiao_line_obj.search(cr , uid, [('invoice_id','=',invoice_id.id),('fapiao_id.state','=','Posted')], context=context)
            for fapiao_line_posted_id in fapiao_line_obj.browse(cr, uid, fapiao_line_posted_ids, context=context) :
                allocated_amount_posted += fapiao_line_posted_id.allocated_ammount
            open_balance = invoice_id.amount_total - allocated_amount_posted
            if open_balance == 0 :
                continue
            else:
                temp.append((0, 0, { 
                    'invoice_id' :  invoice_id.id, 
                    'invoice_date': invoice_id.date_invoice, 
                    'invoice_amount_total': invoice_id.amount_total, 
                    'invoice_state' : invoice_id.state,
                    'full_reconcile' : True,
                    'open_balance_temp' : open_balance,
                    'open_balance' : open_balance,
                    'allocated_ammount' : open_balance,
                    }))
        res['value'] = {
            'fapiao_line_ids' :  temp,
        }
        return res

    def action_validated(self, cr, uid, ids, context=None): 
        for fapiao in self.browse(cr, uid, ids, context):
            for line in fapiao.fapiao_line_ids:
                if line.allocated_ammount:
                    for lines in line.invoice_id.fapiao_line_ids:
                        if lines.fapiao_id.state =='Posted' and lines.full_reconcile:
                            raise orm.except_orm(_('Error!'), _("Line for invoice:'%s' has been reconciled!") % (line.invoice_id.number))
        fapiao_number = self.pool.get('ir.sequence').get(cr, uid, 'fapiao.fwa1') or '/'        
        return self.write(cr, uid, ids, {'state':'Posted', 'name': fapiao_number})
        
    def action_cancel_fapiao(self, cr, uid, ids, context=None): 
        return self.write(cr, uid, ids, {'state':'Draft'})
         
    def onclick_reconcile_all_fapiao(self, cr, uid, ids, context=None):
        fapiao_line_obj = self.pool.get('fapiao.line')
        for fapiao in self.browse(cr, uid, ids, context):
            temp_checkbox = []
            temp_ids = []
            for fapiao_line in fapiao.fapiao_line_ids:
                temp_checkbox.append(fapiao_line.full_reconcile)
                temp_ids.append(fapiao_line.id)
            if False in temp_checkbox:
                for fapiao_line in fapiao.fapiao_line_ids:
                    fapiao_line_obj.write(cr, uid, fapiao_line.id, {'full_reconcile': True, 'allocated_ammount': fapiao_line.open_balance or 0.0}, context)
            else:
                for fapiao_line in fapiao.fapiao_line_ids:
                    fapiao_line_obj.write(cr, uid, fapiao_line.id, {'full_reconcile': False, 'allocated_ammount': 0.0}, context)
        return True
        
#end of fapiao()

class fapiao_tag_line(orm.Model):
    _name = 'fapiao.tag.line'
    _description = "Fapiao Tag Line"
    _columns = {
        'name': fields.char("Name"),
    }
#end of fapiao_tag_line()

class account_invoice(orm.Model):
    _inherit = 'account.invoice'
    
    def _get_lines(self, cr, uid, ids, fields, args, context=None):
        temp = []
        res = {}
        for invoice in self.browse(cr, uid, ids):
            for fapiao_line in invoice.fapiao_line_ids:
                if not fapiao_line.not_fapiao and fapiao_line.fapiao_state == 'Posted' and fapiao_line.allocated_ammount:
                    temp.append(fapiao_line.id)    
            res[invoice.id] = temp
        return res
    
    _columns = {
        'fapiao_line_ids' : fields.one2many('fapiao.line','invoice_id','Fapiao Line'),
        'fapiao_line_ids_display' : fields.function(_get_lines, string='Fapiao Lines', relation="fapiao.line", method=True, type="one2many"),
    }
    
    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        default.update({
            'fapiao_line_ids':[],
        })        
        return super(account_invoice, self).copy(cr, uid, id, default, context)
        
#end of account_invoice()

class fapiao_line(orm.Model):
    _name = 'fapiao.line'
    _description = "Fapiao Line"
    
    def onchange_full_reconcile(self, cr, uid, ids, full_reconcile, open_balance, context=None):
        if context is None:
            context = {}
        res = {}
        if full_reconcile :
            res['value'] = {
                'allocated_ammount' :  open_balance,
            }
        else:
            res['value'] = {
                'allocated_ammount' :  0,
            } 
        return res
    
    def onchange_allocated_ammount(self, cr, uid, ids, allocated_ammount, open_balance, context=None):
        if context is None:
            context = {}
        res = {}
        if allocated_ammount ==  open_balance:
            res['value'] = {
                'full_reconcile' :  True,
            }
        else:
            res['value'] = {
                'full_reconcile' :  False,
            } 
        return res


    def _get_open_balance_temp(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for fapiao_line in self.browse(cr,uid,ids,context=context):
            res[fapiao_line.id] = fapiao_line.open_balance
        return res
        
    _columns = {
        'fapiao_id' : fields.many2one('fapiao','Fapiao', ondelete='cascade',select=1),
        'fapiao_number' : fields.related('fapiao_id','fapiao_number',type="char",string="Fapiao Number",store=False),
        'fapiao_date' : fields.related('fapiao_id','fapiao_date',type="date",string="Fapiao Date",store=False),
        'fapiao_state' : fields.related('fapiao_id','state',type="char",string="Fapiao Status",store=False),
        'invoice_id' : fields.many2one('account.invoice','Invoice',required=True),
        'invoice_date' : fields.related('invoice_id','date_invoice',type="date",string="Invoice Date",store=False),
        'invoice_amount_total' : fields.related('invoice_id','amount_total',type="float",string="Invoice Amount Total",store=False),
        'invoice_state' : fields.related('invoice_id','state',type="char",string="Invoice Status",store=False),
        'full_reconcile' : fields.boolean('Full Reconcile'),
        'allocated_ammount' : fields.float('Allocated Amount'),
        'open_balance_temp' : fields.function(_get_open_balance_temp, digits_compute=dp.get_precision('Account'), string="Open Balance", store=False),
        'open_balance' : fields.float("Open Balance", digits_compute=dp.get_precision('Account')),
        'not_fapiao' : fields.boolean('Not Fapiao'),
    }
    
    def open_invoice(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.browse(cr,uid ,ids)[0]
        return {
            'type': 'ir.actions.act_window',
            'name': data.invoice_id.number,
            'res_model': 'account.invoice',
            'res_id' : data.invoice_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'nodestroy': True,
        }
        
#end of fapiao_line()