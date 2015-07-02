from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from lxml import etree
import time

from openerp import SUPERUSER_ID
from openerp import tools
from openerp import fields, models, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class project(models.Model):
    _name = "project.project"
    _inherit = "project.project"
    
    @api.model
    def _default_date_from(self):
        return time.strftime('%Y-%m-01')

    @api.model
    def _default_date_to(self):
        return (datetime.today() + relativedelta(months=+1,day=1,days=-1)).strftime('%Y-%m-%d')

    #fields start here   
    fal_project_timesheet_budget_line_ids = fields.One2many('fal.project.timesheet.budget.line', 'project_id', string="Budget Planning", copy=False)
    date_start = fields.Date(required=True, default=_default_date_from,)
    date = fields.Date(required=True, default=_default_date_to,)
    #end here
        
#end of project()

class project_task(models.Model):
    _name = "project.task"
    _inherit = "project.task"
    
    @api.one
    @api.depends('work_ids', 'effective_hours', 'fal_project_timesheet_budget_line_ids.unit_amount')
    def _timesheet_budget_planning(self):
        plan_hours = 0.00
        for budget_line in self.fal_project_timesheet_budget_line_ids:
            plan_hours += budget_line.unit_amount
        self.planned_hours = plan_hours
        self.remaining_hours = plan_hours - self.effective_hours
               
    #fields start here   
    fal_project_timesheet_budget_line_ids = fields.One2many('fal.project.timesheet.budget.line', 'task_id', string="Budget Planning", copy=False)
    planned_hours = fields.Float(compute="_timesheet_budget_planning", store=True)
    remaining_hours = fields.Float(compute="_timesheet_budget_planning", store=True)
    #end here
        
#end of project_task()

class fal_project_timesheet_budget_line(models.Model):
    _name = "fal.project.timesheet.budget.line"

    #fields start here        
    date = fields.Date('Date', required=True, select=True)
    project_id = fields.Many2one('project.project', 'Project', ondelete='restrict', select=True,)
    task_id = fields.Many2one('project.task', 'Task', required=True, ondelete='restrict', select=True, domain="[('project_id','=',project_id)]")
    name = fields.Char('Description', required=True)
    unit_amount = fields.Float('Quantity', help='Specifies the amount of quantity to count.')
    user_id = fields.Many2one('res.users', 'User', related="task_id.user_id", store=True, readonly=True)
    #company_id = fields.Many2one('res.company', related="project_id.company_id", string='Company', store=True, readonly=True)
    #end here
    
    @api.multi
    def write(self, vals):
        res = super(fal_project_timesheet_budget_line, self).write(vals)
        if 'project_id' in vals:
            if vals['project_id'] == False:
                self.unlink()
        return res
    
    @api.multi
    def on_change_task_id(self, task_id, user_id=False, unit_amount=0):
        res = {}

        return res
        
    @api.multi
    def multi_on_change_task_id(self, task_ids):
        return dict([(el, self.on_change_task_id(el, self.env.context.get('user_id', self.env.uid))) for el in task_ids])

    @api.model
    def on_change_unit_amount(self,prod_id, quantity, company_id,
            unit=False, journal_id=False):
        res = {}

        return res           
            
#end of fal_project_timesheet_budget_line()
    