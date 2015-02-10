import time
from lxml import etree
from openerp.osv import fields, orm
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.tools.float_utils import float_compare
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _

class quotation_follower_wizard(orm.TransientModel):
    _name = "quotation.follower.wizard"

    _columns = {
        'action_description' : fields.text('Action'),
    }
    
    def confirm(self, cr, uid, ids, context=None):
        data = self.browse(cr, uid ,ids)[0]
        sale_obj = self.pool.get('sale.order')
        if context.get('active_id',False):
            value = sale_obj.browse(cr,uid,context['active_id']).fal_action_counter + 1
            sale_obj.message_post(cr, uid, [context['active_id']], body=data.action_description, context=context)
            sale_obj.write(cr, uid, [context['active_id']], {'fal_action_counter' : value})
        return {'type': 'ir.actions.act_window_close'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
