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
        'project_todo_list' : fields.boolean('To do list'),
        'classic_project' : fields.boolean('Classic Project'),
    }
    
    def _get_type_common(self, cr, uid, context):
        ids = super(project, self)._get_type_common(cr, uid, context)
        if context.get('default_project_todo_list',False):
            ids = self.pool.get('project.task.type').search(cr, uid, [('todolist_default','=',1)], context=context)
        return ids
        
    _defaults = {
        'type_ids': _get_type_common,
    }
#end of project()

class project_task_type(orm.Model):
    _name = 'project.task.type'
    _inherit = 'project.task.type'
    _columns = {
        'todolist_default' : fields.boolean('Default for New To do List',
                        help="If you check this field, this stage will be proposed by default on each new To do List. It will not assign this stage to existing To do List."),
    }
#end of project_task_type()