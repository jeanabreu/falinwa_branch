# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class purchase_order(orm.Model):
    _name = 'purchase.order'
    _inherit = 'purchase.order'

    def action_project_update(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        """Open the project update wizard"""
        context.update({
            'active_model': self._name,
            'active_ids': ids,
            'active_id': len(ids) and ids[0] or False,
        })
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'project.update.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
            'nodestroy': True,
        }
    
#end of purchase_order()