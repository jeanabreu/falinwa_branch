# -*- coding: utf-8 -*-
import time
from datetime import datetime

import openerp.addons.decimal_precision as dp
from openerp.osv import fields, orm
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP
from openerp.tools import float_compare
from openerp.tools.translate import _
from openerp import netsvc
from openerp import tools
from openerp import SUPERUSER_ID
from openerp.addons.product import _common

class mrp_production_workcenter_line(orm.Model):
    _name = 'mrp.production.workcenter.line'
    _inherit = 'mrp.production.workcenter.line'
    
    _columns = {
        'fal_is_manufacture' : fields.boolean('Is Manufacture'),
    }
    
#end of mrp_production_workcenter_line()

class mrp_bom(orm.Model):
    _name = 'mrp.bom'
    _inherit = 'mrp.bom'

    def _bom_explode(self, cr, uid, bom, factor, properties=None, addthis=False, level=0, routing_id=False):
        result, result2 = super(mrp_bom, self)._bom_explode(cr, uid, bom, factor, properties, addthis, level, routing_id)
        result2 = []
        phantom = False
        routing_obj = self.pool.get('mrp.routing')
        if bom.type == 'phantom' and not bom.bom_lines:
            newbom = self._bom_find(cr, uid, bom.product_id.id, bom.product_uom.id, properties)
            if newbom:
                phantom = True
            else:
                phantom = False
        if not phantom:
            result2 = []
            routing = (routing_id and routing_obj.browse(cr, uid, routing_id)) or bom.routing_id or False
            if routing:
                for wc_use in routing.workcenter_lines:
                    wc = wc_use.workcenter_id
                    d, m = divmod(factor, wc_use.workcenter_id.capacity_per_cycle)
                    mult = (d + (m and 1.0 or 0.0))
                    cycle = mult * wc_use.cycle_nbr
                    if wc.time_start:
                        result2.append({
                            'name': 'Setup for ' + tools.ustr(wc_use.name) + ' - '  + tools.ustr(bom.product_id.name),
                            'workcenter_id': wc.id,
                            'sequence': level+(wc_use.sequence-1 or 0),
                            'cycle': 1.0,
                            'hour': wc.time_start or 0.0,
                        })                    
                    result2.append({
                        'name': 'Manufacture for ' + tools.ustr(wc_use.name) + ' - '  + tools.ustr(bom.product_id.name),
                        'workcenter_id': wc.id,
                        'sequence': level+(wc_use.sequence or 0),
                        'cycle': cycle,
                        'hour': float(wc_use.hour_nbr*mult + (cycle*(wc.time_cycle or 0.0)) * (wc.time_efficiency or 1.0)),
                        'fal_is_manufacture' : True,
                    })
                    if wc.time_stop:
                        result2.append({
                            'name': 'Cleaning for ' + tools.ustr(wc_use.name) + ' - '  + tools.ustr(bom.product_id.name),
                            'workcenter_id': wc.id,
                            'sequence': level+(wc_use.sequence+1 or 0),
                            'cycle': 1.0,
                            'hour': wc.time_stop or 0.0,
                        }) 
            for bom2 in bom.bom_lines:
                res = self._bom_explode(cr, uid, bom2, factor, properties, addthis=True, level=level+10)
                result2 = result2 + res[1]
        return result, result2
        
#end of mrp_bom()