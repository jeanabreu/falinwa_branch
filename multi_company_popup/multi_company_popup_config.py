# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _

class popup_after_login_config(orm.TransientModel):
    _name = "popup.after.login.config"
    _description = "After login config"
    
    _columns = {
        'company_id': fields.many2one('res.company', 'Company', required=True,
            help='The company this user is currently working for.',context={'user_preference': True}),
    }
    
    def _get_company(self,cr, uid, context=None, uid2=False):
        if not uid2:
            uid2 = uid
        user_obj = self.pool.get('res.users')
        user = user_obj.read(cr, uid, uid2, ['company_id'], context)
        company_id = user.get('company_id', False)
        return company_id and company_id[0] or False
        
    _defaults = {
        'company_id': _get_company,
    }

    def onchange_company_id(self, cr, uid, ids, company_id):
        user_obj = self.pool.get('res.users')
        if company_id:
            write_temp = {
                'company_id' : company_id,
            }
            user_obj.write(cr,uid,uid,write_temp)
        return True
            
    def execute(self, cr, uid, ids, context=None):
        """
        user_obj = self.pool.get('res.users')
        for config_id in self.browse(cr,uid,ids):
            write_temp = {
                'company_id' : config_id.company_id.id,
            }
            user_obj.write(cr,uid,uid,write_temp)
        """
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        
#end of popup_after_login_config()