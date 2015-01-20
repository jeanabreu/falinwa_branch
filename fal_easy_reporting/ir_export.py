# -*- coding: utf-8 -*-
from openerp.osv import fields,orm


class ir_exports_line(orm.Model):
    _name = 'ir.exports.line'
    _inherit = 'ir.exports.line'
    _order = 'sequence, id'
    _columns = {
        'sequence' : fields.integer('Sequence', help="Used to order the sequences."),
        
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

