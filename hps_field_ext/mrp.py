# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
from openerp import SUPERUSER_ID

class mrp_production(orm.Model):
    _name = 'mrp.production'    
    _inherit = 'mrp.production'      

    def _get_one_fal_production_root_serie_name_id(self, production_id):
        root_serie_name_id = production_id.fal_serie_name_id
        if production_id.fal_parent_mo_id:
            root_serie_name_id = self._get_one_fal_production_root_serie_name_id(production_id.fal_parent_mo_id)
        return root_serie_name_id
            
    def _get_fal_production_root_serie_name_id(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for production_id in self.browse(cr, uid, ids, context=context):
            root_serie_name_id = self._get_one_fal_production_root_serie_name_id(production_id)
            if root_serie_name_id:
                res[production_id.id] = root_serie_name_id.id
            else:
                res[production_id.id] = False
        return res
        
    _columns = {
        'fal_production_root_serie_name_id' : fields.function(_get_fal_production_root_serie_name_id, type='many2one', relation='fal.serie.name', string='Root Production Order Serie Name', store=False),
    }
        
#end of mrp_production()