# -*- coding: utf-8 -*-
import time
from datetime import datetime

import openerp.addons.decimal_precision as dp
from openerp.osv import fields, orm
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP
from openerp.tools import float_compare
from openerp.tools.translate import _
from openerp import netsvc
from openerp import tools
from openerp import SUPERUSER_ID
from openerp.addons.product import _common

class mrp_workcenter(orm.Model):
    _name = 'mrp.workcenter'
    _inherit = 'mrp.workcenter'

    _columns = {
        'time_cycle': fields.float('Time for 1 cycle', help="Time for doing one cycle."),
        'time_start': fields.float('Time before prod.', help="Time for the setup."),
        'time_stop': fields.float('Time after prod.', help="Time for the cleaning."),
        'costs_hour': fields.float('Cost per time', help="Specify Cost of Work Center"),
        'costs_hour_account_id': fields.many2one('account.analytic.account', 'Time Account', domain=[('type','!=','view')],
            help="Fill this only if you want automatic analytic accounting entries on production orders."),
    }
#end of mrp_workcenter()

class mrp_routing_workcenter(orm.Model):
    _name = 'mrp.routing.workcenter'
    _inherit = 'mrp.routing.workcenter'
    
    _columns = {
        'fal_extra_operator' : fields.float('Extra operator', required=True),
        'hour_nbr': fields.float('Number of time', required=True, help="Time for this Work Center to achieve the operation of the specified routing."),
        'fal_minimum_cycle_time' : fields.float('Minimum Cycle Time'),
        'fal_stroke_cycle_time_ref' : fields.float('Stroke Cycle Time Ref'),
    }
    
    _defaults = {
        'fal_extra_operator': lambda *a: 0.0,
    }
    
#end of mrp_routing_workcenter()

class mrp_production_workcenter_line(orm.Model):
    _name = 'mrp.production.workcenter.line'
    _inherit = 'mrp.production.workcenter.line'
    
    def _get_operation_cycle_time(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for production_workcenter_line in self.browse(cr, uid, ids, context=context):
            res[production_workcenter_line.id] = production_workcenter_line.fal_operation_id.fal_minimum_cycle_time
        return res
        
    def _get_operation_stroke_cycle_time_ref(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for production_workcenter_line in self.browse(cr, uid, ids, context=context):
            res[production_workcenter_line.id] = production_workcenter_line.fal_operation_id.fal_stroke_cycle_time_ref
        return res
    
    _columns = {
        'fal_operation_id' : fields.many2one('mrp.routing.workcenter', 'Operation'),
        'fal_operation_minimum_cycle_time' : fields.function(_get_operation_cycle_time, string="Operation Minimum Cycle Time", type="float", store=False),
        'fal_operation_stroke_cycle_time_ref' : fields.function(_get_operation_stroke_cycle_time_ref, string="Operation Stroke Cycle Time Ref", type="float", store=False),
        'hour': fields.float('Number of Time', digits=(16,2)),
        'delay': fields.float('Working Time',help="The elapsed time between operation start and stop in this Work Center",readonly=True),
    }
    
#end of mrp_production_workcenter_line()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
