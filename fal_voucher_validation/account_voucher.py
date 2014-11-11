from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class account_voucher(orm.Model):
    _name = 'account.voucher'
    _inherit = 'account.voucher'
    
    _columns = {
        'state':fields.selection(
            [('draft','Draft'),
             ('cancel','Cancelled'),
             ('validated','Validated'),
             ('proforma','Pro-forma'),
             ('posted','Posted')
            ], 'Status', readonly=True, size=32, track_visibility='onchange',
            help=' * The \'Draft\' status is used when a user is encoding a new and unconfirmed Voucher. \
                        \n* The \'Pro-forma\' when voucher is in Pro-forma status,voucher does not have an voucher number. \
                        \n* The \'Posted\' status is used when user create voucher,a voucher number is generated and voucher entries are created in account \
                        \n* The \'Cancelled\' status is used when user cancel voucher.'),
    }
    
    def action_button_validated(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for voucher_id in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, ids, {
                'state' : 'validated',
                }, context=context)
        return True
        
    def action_button_unvalidated(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for voucher_id in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, ids, {
                'state' : 'draft',
                }, context=context)
        return True
    
#end of account_voucher()