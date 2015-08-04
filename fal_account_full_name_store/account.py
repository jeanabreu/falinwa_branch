from openerp import fields, models, api
from openerp.tools.translate import _

class account_account(models.Model):
    _name = "account.account"
    _inherit = "account.account"

    def _get_fal_one_full_name(self, elmt, level=6):
        #if level<=0:
        #    return '...'
        if elmt.parent_id:
            parent_path = self._get_fal_one_full_name(elmt.parent_id, level-1) + " / "
        else:
            parent_path = ''
        return parent_path + elmt.code + ' ' + elmt.name
        
    @api.one
    @api.depends('name', 'code', 'parent_id', 'parent_id.code', 'parent_id.name', 'parent_id.type', 'parent_id.active')
    def _get_fal_full_name(self):
        children_ids = self.search([('id', 'child_of', self.id)])
        for children_id in children_ids:
            print children_id
            #children_id.write({'fal_complete_name' : self._get_fal_one_full_name(children_id)})
            children_id.fal_complete_name = self._get_fal_one_full_name(children_id)
        
    fal_complete_name = fields.Char(compute=_get_fal_full_name,
                           string='Full Name', readonly=True, store=True)
    
#end of account_account()

class account_analytic_account(models.Model):
    _name = "account.analytic.account"
    _inherit = "account.analytic.account"

    def _get_fal_one_full_name(self, elmt, level=6):
        #if level<=0:
        #    return '...'
        if elmt.parent_id and not elmt.type == 'template':
            parent_path = self._get_fal_one_full_name(elmt.parent_id, level-1) + " / "
        else:
            parent_path = ''
        return parent_path + elmt.name

    @api.one
    @api.depends('name', 'parent_id', 'state', 'parent_id.name', 'parent_id.state')
    def _get_fal_full_name(self):
        self.fal_complete_name = self._get_fal_one_full_name(self)
        
    fal_complete_name = fields.Char(compute=_get_fal_full_name,
                           string='Full Name', readonly=True, store=True)
    
#end of account_analytic_account()