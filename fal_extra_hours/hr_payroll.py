#-*- coding:utf-8 -*-
import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta

from openerp import netsvc
from openerp import fields, models, api
from openerp import tools
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp.tools.safe_eval import safe_eval as eval

class hr_payslip(models.Model):
    _name = 'hr.payslip'
    _inherit = 'hr.payslip'
           
    @api.model
    def get_inputs(self, contract_ids, date_from, date_to):
        res = super(hr_payslip, self).get_inputs(contract_ids, date_from, date_to)
        #extrahours_line_ids = self.get_fal_extrahours_line(contract_ids[0].employee, date_from, date_to)
        #for extrahours_line in self.env['fal.extra.hours.line'].browse(extrahours_lines):            
        #    print 'jalan'
        contract_id = self.env['hr.contract'].browse(contract_ids[0])
        basic_wage = contract_id.wage
        for input in res:
            extrahours_line_ids = self.get_fal_extrahours_line(contract_id.employee_id, date_from, date_to, input['code'])
            for eh_line in extrahours_line_ids:
                if eh_line.salary_rule_input_id.fal_is_extra_hours:
                    working_days = eh_line.fal_extra_hours_id.working_days
                    qty = eh_line.hours
                    rate = eh_line.salary_rule_input_id.fal_rate                               
                    unit_amount = basic_wage / working_days / 8 * rate
                    input['fal_unit_amount'] = unit_amount
                    input['fal_qty'] = qty
                    input['amount'] = unit_amount * qty
                if eh_line.salary_rule_input_id.fal_is_leave:
                    working_days = eh_line.fal_extra_hours_id.working_days
                    qty = eh_line.hours
                    rate = eh_line.salary_rule_input_id.fal_rate                               
                    unit_amount = basic_wage / working_days
                    input['fal_unit_amount'] = - unit_amount
                    input['fal_qty'] = qty
                    input['amount'] = input['fal_unit_amount'] * qty                    
        return res

    @api.model
    def get_fal_extrahours_line(self, employee, date_from, date_to, input_code):
        """
        @param employee: browse record of employee
        @param date_from: date field
        @param date_to: date field
        @param salary_rule_code: salary rule code field
        @return: returns the ids of all the contracts for the given employee that need to be considered for the given dates
        """
        extra_hours_line_obj = self.env['fal.extra.hours.line']
        clause = []
        #a contract is valid if it ends between the given dates
        #clause_1 = ['&',('fal_extra_hours_id.date_to', '<=', date_to),('fal_extra_hours_id.date_to','>=', date_from)]
        #OR if it starts between the given dates
        clause_2 = ['&',('fal_extra_hours_id.date_from', '<=', date_to),('fal_extra_hours_id.date_from','>=', date_from)]
        #OR if it starts before the date_from and finish after the date_end (or never finish)
        #clause_3 = ['&',('fal_extra_hours_id.date_from','<=', date_from),'|',('dfal_extra_hours_id.ate_to', '=', False),('fal_extra_hours_id.date_to','>=', date_to)]
        clause_4 = [('salary_rule_input_id.code','=',input_code)]
        clause_5 = [('salary_rule_input_id.state','=','done')]
        clause_final =  [('employee_id', '=', employee.id)] + clause_2 + clause_4
        extra_hours_ids = extra_hours_line_obj.search(clause_final)
        return extra_hours_ids
    
#end of hr_payslip()


class hr_rule_input(models.Model):
    _name = 'hr.rule.input'
    _inherit = 'hr.rule.input'
    
    #fields start here
    fal_is_extra_hours = fields.Boolean('Is Extra Hours')
    fal_is_leave = fields.Boolean('Is Leave')
    fal_rate = fields.Float('Rate')
    #end here
    
#end of hr_rule_input()

class hr_payslip_input(models.Model):
    _name = 'hr.payslip.input'
    _inherit = 'hr.payslip.input'
    
    #fields start here
    fal_unit_amount = fields.Float('Unit Amount')
    fal_qty = fields.Float('Qty')
    #end here
    
#end of hr_payslip_input()

class fal_extra_hours(models.Model):
    _name = 'fal.extra.hours'
    _description = "Extra Hours"
    _order = "name desc, id desc"
    
    #fields start here
    name = fields.Char("Extra Hours Number", copy=False)
    working_days = fields.Float("Working days", default=21.75, readonly=True, states={'draft': [('readonly', False)]})
    date_from = fields.Date('Date From', readonly=True, states={'draft': [('readonly', False)]}, default=lambda *a: time.strftime('%Y-%m-01'), required=True)
    date_to = fields.Date('Date To', readonly=True, states={'draft': [('readonly', False)]}, default=lambda *a: str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10], required=True)
    state =  fields.Selection([
            ('draft', 'Draft'),
            ('validate', 'Validate'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
        ], 'Status', select=True, readonly=True, default='draft', copy=False)
    fal_extra_hours_line = fields.One2many('fal.extra.hours.line', 'fal_extra_hours_id', string='Extra Hours Line', readonly=True, states={'draft': [('readonly', False)]}, copy=False)
    company_id = fields.Many2one('res.company', 'Company', required=True, readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env['res.company']._company_default_get('fal.extra.hours'))
    #end here

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.pool.get('ir.sequence').get(self.env.cr, self.env.uid, 'fal.extra.hours') or '/'            
        return super(fal_extra_hours, self).create(vals)
    
    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancel'})
        return True
        
    @api.multi
    def action_validate(self):
        self.write({'state': 'validate'})
        return True
        
    @api.multi
    def action_done(self):
        self.write({'state': 'done'})
        return True
        
    @api.multi
    def action_draft(self):
        self.write({'state': 'draft'})
        return True

    @api.multi
    def unlink(self):
        for extra_hours_id in self:
            if extra_hours_id.state not in ('draft', 'cancel'):
                raise Warning(_('You cannot delete an Extra hours which is not draft or cancelled.'))
        return super(fal_extra_hours, self).unlink()
        
#end of fal_extra_hours()

class fal_extra_hours_line(models.Model):
    _name = 'fal.extra.hours.line'
    _description = "Extra Hours Line"
    
    #fields start here
    fal_extra_hours_id = fields.Many2one('fal.extra.hours', 'Extra Hours')
    employee_id = fields.Many2one('hr.employee', 'Employee', required=True)
    salary_rule_input_id = fields.Many2one('hr.rule.input', 'Extra Hours Type', required=True, domain="['|',('fal_is_extra_hours','=',1),('fal_is_leave','=',1)]")
    hours = fields.Float('Qty')
    #end here

#end of fal_extra_hours_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
