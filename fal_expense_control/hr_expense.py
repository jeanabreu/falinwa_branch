import time

from openerp import netsvc
from openerp.osv import fields, orm
from openerp.tools.translate import _

import openerp.addons.decimal_precision as dp

class hr_expense_expense(orm.Model):
    _name = "hr.expense.expense"
    _inherit = "hr.expense.expense"
    
    def onchange_currency_id(self, cr, uid, ids, currency_id=False, company_id=False, context=None):
        res =  {}
        return res
    
    def confirm_all_refund(self, cr, uid, ids, context):
        if context is None:
            context={}
        expense_line_obj = self.pool.get("hr.expense.line")
        for expense_id in self.browse(cr, uid, ids, context):
            temp_confirm = []
            for expense_line in expense_id.line_ids:
                if expense_line.fal_reason_why in ['director', 'employee']:
                    temp_confirm.append(expense_line.fal_confirm_refund)
            if False in temp_confirm:
                for expense_line in expense_id.line_ids:
                    if expense_line.fal_reason_why in ['director', 'employee'] and expense_line.fal_accepted_amount > expense_line.fal_budget:
                        expense_line_obj.write(cr, uid, [expense_line.id], {'unit_amount' : expense_line.fal_accepted_amount, 'fal_confirm_refund': True}, context)
            else:
                for expense_line in expense_id.line_ids:
                    if expense_line.fal_reason_why in ['director', 'employee'] :
                        expense_line_obj.write(cr, uid, [expense_line.id], {'unit_amount' : expense_line.fal_budget, 'fal_confirm_refund': False}, context)
        return True
    
#end of hr_expense_expense()

class hr_expense_line(orm.Model):
    _name = "hr.expense.line"
    _inherit = "hr.expense.line"
    
    def _get_expense_control(self, cr, uid, ids, field_name, arg, context=None):
        if context is None:
            context = {}
        res = {}
        for expense_line in self.browse(cr, uid, ids, context=context):
            res[expense_line.id] = 'No Control'
            if expense_line.product_id:
                total_budget = expense_line.product_id.expense_budget * expense_line.fal_quantity
                if expense_line.product_id.expense_budget == 0.00:
                    res[expense_line.id] = 'No Control'
                elif expense_line.unit_amount < total_budget :
                    res[expense_line.id] = 'In Budget'
                elif expense_line.unit_amount == total_budget :
                    res[expense_line.id] = 'Max Budget'
                else:
                    res[expense_line.id] = 'Out Budget'
        return res
        
    def _get_budget(self, cr, uid, ids, field_name, arg, context=None):
        if context is None:
            context = {}
        res = {}
        for expense_line in self.browse(cr, uid, ids, context=context):
            res[expense_line.id] = 0.00
            if expense_line.product_id:
                res[expense_line.id] = expense_line.product_id.expense_budget * expense_line.fal_quantity
        return res
    
    def _get_currency(self, cr, uid, context=None):
        user_obj = self.pool.get('res.users')
        currency_obj = self.pool.get('res.currency')
        user = user_obj.browse(cr, uid, uid, context=context)

        if user.company_id:
            return user.company_id.currency_id.id
        else:
            return currency_obj.search(cr, uid, [('rate', '=', 1.0)])[0]
            
    def _get_accepted_amount(self, cr, uid, ids, field_name, arg, context=None):
        if not ids:
            return {}
        cr.execute("SELECT l.id,COALESCE(SUM(l.fal_real_amount*l.unit_quantity),0) AS amount FROM hr_expense_line l WHERE id IN %s GROUP BY l.id ",(tuple(ids),))
        res = dict(cr.fetchall())
        return res
        
    _columns = {
        'product_id': fields.many2one('product.product', 'Product', domain=[('hr_expense_ok','=',True)], required=True),
        'unit_amount': fields.float('Price', digits_compute=dp.get_precision('Product Price')),
        'fal_expense_control' : fields.function(_get_expense_control, type='char', string='Expense Control', store=True),
        'fal_budget' : fields.function(_get_budget, type='float', digits_compute=dp.get_precision('Product Price'), string='Budget', store=True),
        'fal_real_amount': fields.float('Real Price', digits_compute=dp.get_precision('Product Price')),
        'fal_real_currency' : fields.many2one('res.currency','Real Currency', required=True),
        'fal_accepted_amount' : fields.function(_get_accepted_amount, type='float', string='Accepted Amount', digits_compute=dp.get_precision('Product Price'), store=True),
        'fal_reason_why' : fields.selection([('customer','With Customer'), ('manager','With Manager'), ('director','Require Refund To Director'), ('employee','Require at Employee Charge')], string="Reason"),
        'fal_reason' : fields.text('Explanation'),
        'fal_document_currency_id' : fields.many2one('res.currency', 'Document Currency'),
        'fal_quantity' : fields.float('Quantity', digits_compute= dp.get_precision('Product Unit of Measure')),
        'fal_confirm_refund' : fields.boolean('Confirm Refund'),
        'fal_state' : fields.related('expense_id', 'state', type='char', string="State", store=False),
    }
    
    _defaults = {
        'fal_expense_control' : 'No Control',
        'fal_real_currency': _get_currency,
        'fal_quantity': 1,
    }
    
    def onchange_product_id(self, cr, uid, ids, product_id, context=None):
        res = super(hr_expense_line, self).onchange_product_id(cr, uid, ids, product_id, context = context)
        if product_id:
            product = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
            res['value']['fal_real_amount'] = product.price_get('standard_price')[product.id]
            res['value']['fal_budget'] = product.expense_budget
        return res
        
    def onchange_date_amount_cur(self, cr, uid, ids, product_id, date_value, fal_real_amount, fal_real_currency, context):
        res = {'value': {}}
        cur_obj = self.pool.get('res.currency')
        ctx = context.copy()
        ctx.update({'date': date_value})
        if date_value:
            if fal_real_currency:
                real_cur_id = cur_obj.browse(cr, uid, fal_real_currency, context)
                cur_id = cur_obj.browse(cr, uid, ctx['currency_id'], context)
                temp = fal_real_amount
                if real_cur_id != cur_id:
                    temp = cur_obj.compute(cr, uid, real_cur_id.id, cur_id.id, temp, context=ctx)
                res['value']['unit_amount'] = cur_obj.round(cr, uid, cur_id, temp)
        return res    
    
    def onchange_quantity(self, cr, uid, ids, product_id, fal_quantity, fal_budget, context=None):
        res = {'value': {},'warning':{}}
        if product_id and fal_quantity:
            product = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
            res['value']['fal_budget'] = product.expense_budget * fal_quantity
        return res
        
    def onchange_unit_price(self, cr, uid, ids, unit_amount, fal_budget, context):
        res = {'value': {},'warning':{}}
        cur_obj = self.pool.get('res.currency')
        warning_msgs = ''

        cur_id = cur_obj.browse(cr, uid, context.get('currency_id',1))
        if fal_budget == 0.00:
            res['value']['fal_expense_control'] = 'No Control'
        elif unit_amount < fal_budget :
            res['value']['fal_expense_control'] = 'In Budget'
        elif unit_amount == fal_budget :
            warning_msgs = _('This line has a budget: %s %s, Budget amount is at maximum. By Confirm it you ensure that you really spent this amount during your mission!') % (fal_budget, cur_id.symbol)
            res['value']['fal_expense_control'] = 'Max Budget'
        else:
            warning_msgs = _('This line has a budget: %s %s, You are out of budget!') % (fal_budget, cur_id.symbol)
            res['value']['fal_expense_control'] = 'Out Budget'
            """
            return {
                'type': 'ir.actions.act_window',
                'name': 'Reason',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'fal.expense.line.reason.wizard',
                'nodestroy': True,
            }
            """
        if warning_msgs:
            warning = {
                       'title': _('Warning!'),
                       'message' : warning_msgs
                    }
            res['warning'] = warning
        return res

    def create(self, cr, uid, vals, context=None):
        product_obj = self.pool.get('product.product')
        product_id = product_obj.browse(cr, uid, vals['product_id'])
        if vals.get('fal_reason_why',False) and vals.get('fal_reason', False) and product_id.expense_budget:
            if vals['fal_reason_why'] in ['director', 'employee']:
                vals['unit_amount'] = product_id.expense_budget * vals['fal_quantity']
        return super(hr_expense_line, self).create(cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context=None):
        product_obj = self.pool.get('product.product')
        for expense_line in self.browse(cr, uid, ids):
            fal_reason_why = vals.get('fal_reason_why',expense_line.fal_reason_why)
            fal_reason = vals.get('fal_reason', expense_line.fal_reason)
            fal_qty = vals.get('fal_quantity', expense_line.fal_quantity)
            product_id = expense_line.product_id
            if vals.get('product_id',False):
                product_id = product_obj.browse(cr, uid, vals['product_id'])
                if fal_reason_why and fal_reason and product_id.expense_budget:
                    if fal_reason_why in ['director', 'employee']:
                        vals['unit_amount'] = product_id.expense_budget * fal_qty
                continue
            if vals.get('fal_real_amount',False) or vals.get('fal_reason_why',False) or vals.get('fal_quantity',False):
                if fal_reason_why and fal_reason and product_id.expense_budget:
                    if fal_reason_why in ['director', 'employee']:
                        vals['unit_amount'] = product_id.expense_budget * fal_qty
                continue
        return super(hr_expense_line, self).write(cr, uid, ids, vals, context)

    def confirm_refund(self, cr, uid, ids, context):
        if context is None:
            context={}
        for expense_line in self.browse(cr, uid, ids, context):
            if expense_line.fal_reason_why in ['director', 'employee'] and expense_line.fal_accepted_amount > expense_line.fal_budget and expense_line.fal_confirm_refund == False:
                self.write(cr, uid, [expense_line.id], {'unit_amount' : expense_line.fal_accepted_amount, 'fal_confirm_refund': True}, context)
            else:
                self.write(cr, uid, [expense_line.id], {'unit_amount' : expense_line.fal_budget, 'fal_confirm_refund': False}, context)
        return True

#end of hr_expense_line()


class product_product(orm.Model):
    _name = "product.product"
    _inherit = "product.product"
    
    _columns = {
        'expense_budget' : fields.float('Expense Budget in CCR'),   
    }
    
#end of product_product()