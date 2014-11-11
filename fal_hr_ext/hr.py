#-*- coding:utf-8 -*-
import time
from openerp import netsvc
from datetime import date, datetime, timedelta

from openerp.osv import fields, orm
from openerp.tools import config, float_compare
from openerp.tools.translate import _

class hr_employee(orm.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"

    _columns = {
        'fal_reference': fields.char('Reference'),
        'address_home_id': fields.many2one('res.partner', 'Related Partner'),
        'driving_license_number': fields.char('Driving License Number', size=128),
        'parents_address': fields.text('Parents Address'),
        'parents_phone': fields.char('Parents Phone', size=64),
        'contact': fields.char('Contact in Case of Accident', size=64),
        'relation_contact': fields.char('Relation of the Contact', size=64),
        'phone_contact': fields.char('Phone of the Contact', size=64),
        'hukou_place': fields.char('Hukou Place', size=128),
        'fal_child_ids': fields.one2many('hr.employee.child', 'employee_id', 'Children')
    }

#end of hr_employee()

class hr_employee_child(orm.Model):
    _name = "hr.employee.child"

    _columns = {
        'employee_id': fields.many2one('hr.employee', string="Employee"),
        'name': fields.char('Name', size=128, required=True, select=True),
    }
    
#end of hr_employee_child()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
