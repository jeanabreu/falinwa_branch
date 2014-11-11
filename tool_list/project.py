from datetime import datetime, date, timedelta
from lxml import etree
import time

from openerp import SUPERUSER_ID
from openerp import tools
from openerp.osv import fields, orm
from openerp.tools.translate import _

from openerp.addons.resource.faces import task as Task

class project(orm.Model):
    _name = "project.project"
    _inherit = "project.project"
    
    _columns = {
        'tasks': fields.one2many('project.task', 'project_id', "Tools Activities"),
        'type_ids': fields.many2many('project.task.type', 'project_task_type_rel', 'project_id', 'type_id', 'Tools Stages', states={'close':[('readonly',True)], 'cancelled':[('readonly',True)]}),
    }
#end of project()

class task(orm.Model):
    _name = "project.task"
    _description = "Tools"
    _inherit = "project.task"
    
    def _get_color_view(self, cr, uid, ids=False, context=None):
        if not ids:
            ids = self.search(cr, uid, [])
        return self.get_color_view(cr, uid, ids, context=context)
        
    def get_color_view(self, cr, uid, ids, context=None):
        res = {}
        for tools in self.browse(cr, uid, ids, context=context):            
            #white:0, red:2, blue:7 , yellow:3
            color = 0
                               
            if tools.date_deadline:
                date_deadline = datetime.strptime(tools.date_deadline, '%Y-%m-%d').date()
                if date_deadline - date.today() >= timedelta(1) and date_deadline - date.today() <= timedelta(7) and not tools.date_deadline_re:
                    color = 3
                elif date_deadline - date.today() <= timedelta(0) and not tools.date_deadline_re:
                    color = 2
                    
            if tools.shipment_date_ex:
                shipment_date_ex = datetime.strptime(tools.shipment_date_ex, '%Y-%m-%d').date()
                if shipment_date_ex - date.today() >= timedelta(1) and shipment_date_ex - date.today() <= timedelta(7) and not tools.shipment_date_re:
                    color = 3
                elif shipment_date_ex - date.today() <= timedelta(0) and not tools.shipment_date_re:
                    color = 2   
                    
            if tools.t_one_date_ex:
                t_one_date_ex = datetime.strptime(tools.t_one_date_ex, '%Y-%m-%d').date()
                if t_one_date_ex - date.today() >= timedelta(1) and t_one_date_ex - date.today() <= timedelta(7) and not tools.t_one_date_re:
                    color = 3
                elif t_one_date_ex - date.today() <= timedelta(0) and not tools.t_one_date_re:
                    color = 2
                             
                    
            self.write(cr , uid, tools.id, {'color': color})
        return True
    
    _columns = {
        'tool_number' : fields.char('Tool Number', size=64),
        'name': fields.char('Tool Summary', size=128, required=True, select=True),
        'parent_ids': fields.many2many('project.task', 'project_task_parent_rel', 'task_id', 'parent_id', 'Parent Tools'),
        'child_ids': fields.many2many('project.task', 'project_task_parent_rel', 'parent_id', 'task_id', 'Delegated Tools'),
        'date_deadline': fields.date('Expected Completion Date', select=True, track_visibility='onchange'),
        't_one_date_ex': fields.date('Expected T1 Date', select=True, track_visibility='onchange'),
        'shipment_date_ex': fields.date('Expected Shipment Date', select=True, track_visibility='onchange'),
        'date_deadline_re': fields.date('Realized Completion Date', select=True, track_visibility='onchange'),
        't_one_date_re': fields.date('Realized T1 Date', select=True, track_visibility='onchange'),
        'shipment_date_re': fields.date('Realized Shipment Date', select=True, track_visibility='onchange'),
        'part_quantity' : fields.char('Part Quantity(for Proto)', size=64),
        'tool_list_destination_id' : fields.many2one('tool.list.destination', 'Tool List Destination'),
        'tool_list_destination_id_name' : fields.related('tool_list_destination_id', 'name', type='char',string='Tool List Destination Name'),
        'production_site_id' : fields.many2one('res.partner','Production Site', domain="[('production_site', '=', True)]"),
    }
    
    def create(self, cr, uid, vals, context=None):
        seqnumber = self.pool.get('ir.sequence').get(cr, uid, 'tools.fwa1')
        if not vals.get('tool_number',False) :
            vals['tool_number'] = seqnumber
        return super(task, self).create(cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context=None):
        project_task_type_obj = self.pool.get('project.task.type')
        if vals.get('stage_id',False):
            task_type_id = project_task_type_obj.browse(cr, uid, vals['stage_id'], context)
            if task_type_id.name == 'T1/Part Validation' :
                vals['t_one_date_re'] = fields.datetime.now()
            if task_type_id.name == 'Shipment' :
                vals['shipment_date_re'] = fields.datetime.now()
            if task_type_id.name == 'Done':
                vals['date_deadline_re'] = fields.datetime.now()
        return super(task, self).write(cr, uid, ids, vals, context=context)

    def onchange_dest(self, cr, uid, id, tool_list_destination_id, context=None):
        result = {}
        if tool_list_destination_id:
            dest = self.pool.get('tool.list.destination').browse(cr, uid, tool_list_destination_id, context=context)
            result['tool_list_destination_id_name'] = dest.name
        return {'value': result}        
#end of task()

class project_work(orm.Model):
    _name = "project.task.work"
    _inherit = "project.task.work"
    
    _columns = {
        'task_id': fields.many2one('project.task', 'Tools', ondelete='cascade', required=True, select="1"),
    }
#end of project_work()

class account_analytic_account(orm.Model):
    _inherit = 'account.analytic.account'
    
    _columns = {
        'use_tasks': fields.boolean('Tools',help="If checked, this contract will be available in the project menu and you will be able to manage tasks or track issues"),
    }
#end of account_analytic_account()

class project_task_history(orm.Model):
    _name = 'project.task.history'
    _inherit = 'project.task.history'
    
    _columns = {
        'task_id': fields.many2one('project.task', 'Tools', ondelete='cascade', required=True, select=True),
    }
#end of project_task_history()

class tool_list_destination(orm.Model):
    _name = 'tool.list.destination'
    _description = "Tool List Destination"
    
    _columns = {
        'name' : fields.char('Name',size=128, required=True)
    }
#end of tool_list_destination()

class res_partner(orm.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    _columns = {
        'production_site' : fields.boolean('Production Site'),
    }
#end of res_partner()