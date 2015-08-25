# -*- coding: utf-8 -*-
from openerp.osv import fields, orm, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp import api

class crm_lead(orm.Model):
    _name = "crm.lead"
    _inherit = "crm.lead"
    
    _columns = {
        'create_date': fields.datetime('Creation Date', readonly=False),
        'date_closed': fields.datetime('Closed', readonly=False, copy=False),
        'fal_project_id' : fields.many2one('project.project', 'Project'),
        'fal_tool_number': fields.char('Tool Number', size=128),
        'fal_t1_date': fields.date('T1 Date'),
        'fal_hps_serie': fields.char('HPS Serie', size=128),
        'fal_qty': fields.char('HPS Serie', size=128),
        'fal_customer_code': fields.char('Customer Code', size=128),
        'fal_old_budget_number': fields.char('Budget Number', size=128),
        'fal_tag_product_range_ids' : fields.many2many('fal.tag.product.range', 'lead_tag_product_range_rel', 'crm_id', 'tag_product_range_id', 'Tag Product Range'),
        'fal_delivery_week': fields.char('Tool Number', size=128),
    }
    
#end of crm_lead()

class res_partner(orm.Model):
    _name = "res.partner"
    _inherit = "res.partner"
    
    _columns = {
        'fal_tag_activity_ids' : fields.many2many('fal.tag.activity', 'res_partner_tag_activity_rel', 'partner_id', 'tag_activity_id','Tag Activity'),
        'fal_tag_product_range_ids' : fields.many2many('fal.tag.product.range', 'res_partner_tag_product_range_rel', 'partner_id', 'tag_product_range_id', 'Tag Product Range'),
    }
    
    _sql_constraints = [
        ('name_email_uniq', 'unique (name,email)', 'The name and email already existed !')
    ]
#end of res_partner()

class fal_tag_activity(orm.Model):
    _description = 'Falinwa tag activity'
    _name = 'fal.tag.activity'
    _columns = {
        'name': fields.char('Activity Name', required=True, translate=True),
    }
    
#end of fal_tag_activity()

class fal_tag_product_range(orm.Model):
    _description = 'Falinwa tag product range'
    _name = 'fal.tag.product.range'
    _columns = {
        'name': fields.char('Product Range', required=True, translate=True),
    }
    
#end of fal_tag_product_range()
