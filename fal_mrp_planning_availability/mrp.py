# -*- coding: utf-8 -*-
from openerp import fields, models, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
from openerp import SUPERUSER_ID

class mrp_production(models.Model):
    _name = 'mrp.production'
    _inherit = 'mrp.production'
    
    fal_floating_production_date = fields.Date("Floating Production Date", readonly=True, states=dict.fromkeys(['draft', 'confirmed'], [('readonly', False)]), copy=False)

#end of mrp_production()

class stock_move(models.Model):
    _name = "stock.move"
    _inherit = "stock.move"
    
    @api.multi
    def action_assign(self):
        new_self = self.filtered(lambda r: r.raw_material_production_id == False) | self.filtered('raw_material_production_id.fal_floating_production_date').filtered(lambda r: r.state == 'confirmed').sorted(key=lambda r: r.raw_material_production_id.fal_floating_production_date, reverse=True)
        for rec in new_self:        
            print str(rec.raw_material_production_id.fal_floating_production_date) + ':' + rec.raw_material_production_id.name
        super(stock_move, new_self).action_assign()
                    
#end of stock_move()