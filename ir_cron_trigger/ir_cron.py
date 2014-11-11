from openerp.osv import fields, orm
from openerp.tools.translate import _

def str2tuple(s):
    return eval('tuple(%s)' % (s or ''))
    
class ir_cron(orm.Model):
    _name = "ir.cron"
    _inherit = "ir.cron"

    def trigger_scheduller(self, cr, uid, ids, context=None):
        for cron in self.browse(cr,uid,ids):
            user = cron.user_id.id
            obj = self.pool.get(cron.model)
            args = str2tuple(cron.args) 
            func = cron.function
            method = getattr(obj, func)
        return method(cr, uid, *args)        
#end of ir_cron()