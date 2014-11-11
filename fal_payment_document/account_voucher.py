from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class account_voucher(orm.Model):
    _name = 'account.voucher'
    _inherit = 'account.voucher'
    
    def action_payment_sent(self, cr, uid, ids, context=None):
        '''
        This function opens a window to compose an email, with the edi invoice template message loaded by default
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        ir_model_data = self.pool.get('ir.model.data')
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'fal_payment_document', 'email_template_payment')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict(context)
        ctx.update({
            'default_model': 'account.voucher',
            'default_res_id': ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_invoice_as_sent': True,
            })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
        
#end of account_voucher()