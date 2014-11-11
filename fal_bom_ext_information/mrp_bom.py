# -*- coding: utf-8 -*-

import base64
from cStringIO import StringIO
import csv
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp import netsvc

class mrp_bom(orm.Model):
    _name = 'mrp.bom'
    _inherit='mrp.bom'
    
    _columns = {
        'fal_part_weight' : fields.float('Part Weight'),
        'fal_regrind' : fields.float('Regrind/Spure Weight'),
        'fal_mold_information_ids' : fields.one2many('fal.mold.line','fal_bom_id','Mold Information'),
    }
        
#end of mrp_bom()

class mrp_production(orm.Model):
    _name = 'mrp.production'
    _inherit = 'mrp.production'
    
    _columns = {
        'project_number' : fields.char('Project Number',size=128),
    }
    
#end of mrp_production()

class fal_mold_information_line(orm.Model):
    _name = 'fal.mold.line'
    
    _columns = {
        'fal_bom_id' : fields.many2one('mrp.bom','BoM'),
        'fal_mold_number' : fields.char('Mold Number', size=128),
        'fal_tonnage' : fields.float('Tonnage (T)'),
        'fal_cycles_time' : fields.float('Cycles Time (S)'),
        'fal_cavity' : fields.char('Cavity', size=128),
    }
        
#end of fal_mold_information_line()

class procurement_order(orm.Model):
    _name = 'procurement.order'
    _inherit = 'procurement.order'
    
    def make_mo(self, cr, uid, ids, context=None):
        """ Make Manufacturing(production) order from procurement
        @return: New created Production Orders procurement wise 
        """
        res = super(procurement_order, self).make_mo(cr, uid, ids, context)
        company = self.pool.get('res.users').browse(cr, uid, uid, context).company_id
        production_obj = self.pool.get('mrp.production')
        move_obj = self.pool.get('stock.move')
        wf_service = netsvc.LocalService("workflow")
        procurement_obj = self.pool.get('procurement.order')
        for procurement in procurement_obj.browse(cr, uid, ids, context=context):
            if procurement.sale_order_line_id and procurement.sale_order_line_id.order_id:
                production_obj.write(cr, uid, res[procurement.id], {'project_number': procurement.sale_order_line_id.order_id.project_id.code}, context=context)
        return res

#end of procurement_order()