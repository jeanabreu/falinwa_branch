#-*- coding:utf-8 -*-
from openerp.osv import fields, orm
from openerp import tools
from openerp.tools.translate import _

class hr_contract(orm.Model):
    _name = 'hr.contract'
    _inherit = 'hr.contract'

    _columns = {
        'fal_company_id': fields.many2one('res.company', 'Company', select=1, help="Company related to this contract"),
    }

    _defaults = {
        'fal_company_id': False,
    }


#end of hr_contract()

class hr_payslip_run(orm.Model):
    _name = 'hr.payslip.run'
    _inherit = 'hr.payslip.run'

    _columns = {
        'fal_company_id': fields.many2one('res.company', 'Company', select=1, help="Company related to this contract"),
    }

    _defaults = {
        'fal_company_id': False,
    }


#end of hr_payslip_run()