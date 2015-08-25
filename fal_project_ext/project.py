from datetime import datetime, date, timedelta
from lxml import etree
import time

from openerp import SUPERUSER_ID
from openerp import tools
from openerp.osv import fields, orm
from openerp.tools.translate import _

class project(orm.Model):
    _name = "project.project"
    _inherit = "project.project"
    
    _columns = {
        'program_name' : fields.char('Program Name',size=128),
        'mold_serial_number' : fields.char('Total Mold Qty',size=128),
        'project_opportunities' : fields.boolean('Opportunities'),
        'classic_project' : fields.boolean('Classic Project'),
    }
    
    def _get_type_common(self, cr, uid, context):
        ids = super(project, self)._get_type_common(cr, uid, context)
        if context.get('default_project_opportunities',False):
            ids = self.pool.get('project.task.type').search(cr, uid, [('project_opportunities_default','=',1)], context=context)
        return ids
        
    _defaults = {
        'type_ids': _get_type_common,
    }
        
#end of project()

class project_task_type(orm.Model):
    _name = 'project.task.type'
    _inherit = 'project.task.type'
    _columns = {
        'project_opportunities_default' : fields.boolean('Default for Project Opportunities',
                        help="If you check this field, this stage will be proposed by default on each new Project Opportunities. It will not assign this stage to existing Project Opportunities."),
    }
#end of project_task_type()

class task(orm.Model):
    _name = "project.task"
    _inherit = "project.task"
    
    _columns = {
        'partner_id': fields.many2one('res.partner', 'Customer'),
        'project_id_partner_id' : fields.related('project_id','partner_id',type='many2one', relation='res.partner', string="Final Customer", readonly=True, store=True)
    }

    def onchange_project(self, cr, uid, id, project_id, context=None):
        res = super(task, self).onchange_project(cr, uid, id, project_id, context=context)
        return {}
        
    _defaults = {
        'partner_id': False
    }
    
    def write(self, cr, uid, ids, vals, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        if vals and not 'kanban_state' in vals and 'stage_id' in vals:
            for t in self.browse(cr, uid, ids, context=context):
                vals['kanban_state'] = t.kanban_state        
                super(task, self).write(cr, uid, [t.id], vals, context=context)
        else:
            result = super(task, self).write(cr, uid, ids, vals, context=context)
        return True
#end of task()

class account_analytic_account(orm.Model):
    _name = 'account.analytic.account'
    _inherit = 'account.analytic.account'
    
    def _get_one_full_name(self, elmt, level=6):
        res = super(account_analytic_account, self)._get_one_full_name(elmt, level)
        if elmt.partner_id:
            res += ' / ' + elmt.partner_id.name
        return res
        
#end of account_analytic_account()
